"""Safe SQL query executor for admin mode analytics."""

import logging
import re
from typing import Any, ClassVar

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class QueryExecutionError(Exception):
    """Exception raised when query execution fails."""


class QueryExecutor:
    """Safe SQL query executor with validation."""

    # Keywords that are not allowed in queries
    FORBIDDEN_KEYWORDS: ClassVar[list[str]] = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "GRANT",
        "REVOKE",
    ]

    def __init__(self, session: AsyncSession) -> None:
        """Initialize query executor.

        Args:
            session: Database session for query execution
        """
        self.session = session

    def validate_query(self, query: str) -> bool:
        """Validate that query is safe to execute.

        Args:
            query: SQL query to validate

        Returns:
            True if query is safe, False otherwise
        """
        # Remove comments and normalize whitespace
        query_normalized = re.sub(r"--.*$", "", query, flags=re.MULTILINE)
        query_normalized = re.sub(r"/\*.*?\*/", "", query_normalized, flags=re.DOTALL)
        query_normalized = " ".join(query_normalized.split()).upper()

        # Check for forbidden keywords (as whole words, not substrings)
        for keyword in self.FORBIDDEN_KEYWORDS:
            # Use word boundaries to match whole words only
            # This prevents false positives like "is_deleted" matching "DELETE"
            if re.search(r"\b" + keyword + r"\b", query_normalized):
                logger.warning(f"Query rejected: contains forbidden keyword '{keyword}'")
                return False

        # Must start with SELECT
        if not query_normalized.strip().startswith("SELECT"):
            logger.warning("Query rejected: does not start with SELECT")
            return False

        return True

    async def execute_query(self, query: str, max_rows: int = 100) -> dict[str, Any]:
        """Execute SELECT query safely and return results.

        Args:
            query: SQL query to execute (must be SELECT)
            max_rows: Maximum number of rows to return

        Returns:
            Dictionary with query results:
            {
                "success": bool,
                "rows": list of dicts,
                "row_count": int,
                "columns": list of column names,
                "error": optional error message
            }

        Raises:
            QueryExecutionError: If query validation or execution fails
        """
        # Validate query
        if not self.validate_query(query):
            raise QueryExecutionError("Query validation failed: contains forbidden operations")

        try:
            # Execute query with LIMIT
            query_with_limit = f"{query.rstrip(';')} LIMIT {max_rows}"
            result = await self.session.execute(text(query_with_limit))

            # Fetch results
            rows = result.fetchall()
            columns = list(result.keys()) if rows else []

            # Convert rows to list of dicts
            rows_as_dicts = [dict(zip(columns, row, strict=True)) for row in rows]

            logger.info(
                f"Query executed successfully: {len(rows_as_dicts)} rows returned, "
                f"columns={columns}"
            )

            return {
                "success": True,
                "rows": rows_as_dicts,
                "row_count": len(rows_as_dicts),
                "columns": columns,
            }

        except Exception as e:
            error_msg = f"Query execution failed: {e!s}"
            logger.error(error_msg)
            return {
                "success": False,
                "rows": [],
                "row_count": 0,
                "columns": [],
                "error": error_msg,
            }

    def format_results_for_llm(self, results: dict[str, Any]) -> str:
        """Format query results for LLM consumption.

        Args:
            results: Query execution results

        Returns:
            Formatted string representation of results
        """
        if not results["success"]:
            return f"Query execution failed: {results.get('error', 'Unknown error')}"

        if results["row_count"] == 0:
            return "Query executed successfully, but returned no rows."

        # Format as a readable text
        output = [f"Query returned {results['row_count']} rows:\n"]

        # Add column headers
        columns = results["columns"]
        output.append(" | ".join(columns))
        output.append("-" * (len(" | ".join(columns))))

        # Add rows
        for row in results["rows"][:10]:  # Show first 10 rows
            row_values = [str(row.get(col, "NULL")) for col in columns]
            output.append(" | ".join(row_values))

        if results["row_count"] > 10:
            output.append(f"\n... and {results['row_count'] - 10} more rows")

        return "\n".join(output)
