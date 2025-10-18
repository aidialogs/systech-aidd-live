"""Admin chat handler with text2sql capabilities."""

import logging

from src.exceptions import LLMError
from src.message import Message
from src.protocols import LLMClientProtocol
from src.query_executor import QueryExecutionError, QueryExecutor

logger = logging.getLogger(__name__)

# Text2SQL prompt template
TEXT2SQL_SYSTEM_PROMPT = """You are a SQL query generator for a chat application database.

Database schema:
- Table: users
  - id (INTEGER, PRIMARY KEY) - User ID from Telegram
  - created_at (TIMESTAMP) - When user was created
  - is_deleted (BOOLEAN) - Soft delete flag

- Table: messages
  - id (INTEGER, PRIMARY KEY, AUTOINCREMENT) - Message ID
  - user_id (INTEGER, FOREIGN KEY -> users.id) - User who sent/received the message
  - chat_id (INTEGER) - Chat identifier (positive for Telegram, negative for web)
  - role (VARCHAR) - Message role: 'system', 'user', or 'assistant'
  - content (TEXT) - Message content
  - content_length (INTEGER) - Length of message content
  - created_at (TIMESTAMP) - When message was created
  - is_deleted (BOOLEAN) - Soft delete flag

Your task: Generate a valid PostgreSQL SELECT query to answer the user's question.
Return ONLY the SQL query, no explanations, no markdown, no extra text.
Always filter out deleted records with: WHERE is_deleted = FALSE"""

ANSWER_SYSTEM_PROMPT = """You are a helpful data analyst assistant.
You will be given a user's question and the results of a SQL query that answers it.
Provide a clear, concise answer to the user's question based on the data.
Format numbers nicely and provide context where helpful."""


class AdminChatHandler:
    """Handler for admin mode with text2sql capabilities."""

    def __init__(
        self,
        llm_client: LLMClientProtocol,
        query_executor: QueryExecutor,
    ) -> None:
        """Initialize admin chat handler.

        Args:
            llm_client: LLM client for generating SQL and answers
            query_executor: Query executor for safe SQL execution
        """
        self.llm_client = llm_client
        self.query_executor = query_executor

    async def handle_analytics_question(self, question: str) -> tuple[str, str]:
        """Handle analytics question using text2sql pipeline.

        Pipeline:
        1. User question → Generate SQL prompt
        2. LLM generates SQL query
        3. Execute query against database
        4. Format results
        5. Pass results to LLM for natural language response

        Args:
            question: User's analytics question

        Returns:
            Tuple of (answer, sql_query)

        Raises:
            LLMError: If LLM request fails
            QueryExecutionError: If query execution fails
        """
        logger.info(f"Admin analytics question: {question}")

        # Step 1: Generate SQL query
        try:
            sql_query = await self._generate_sql_query(question)
            logger.info(f"Generated SQL query: {sql_query}")
        except Exception as e:
            logger.error(f"Failed to generate SQL query: {e!s}")
            raise LLMError(f"Failed to generate SQL query: {e!s}") from e

        # Step 2: Execute query
        try:
            results = await self.query_executor.execute_query(sql_query)

            if not results["success"]:
                error_msg = results.get("error", "Unknown error")
                return (
                    f"Sorry, I couldn't execute the query. Error: {error_msg}",
                    sql_query,
                )

        except QueryExecutionError as e:
            logger.error(f"Query execution failed: {e!s}")
            return (
                f"Sorry, the query couldn't be executed safely: {e!s}",
                sql_query,
            )

        # Step 3: Format results for LLM
        formatted_results = self.query_executor.format_results_for_llm(results)

        # Step 4: Generate natural language answer
        try:
            answer = await self._generate_answer(question, formatted_results)
            logger.info("Generated natural language answer")
            return answer, sql_query

        except Exception as e:
            logger.error(f"Failed to generate answer: {e!s}")
            # Fallback: return formatted results directly
            return formatted_results, sql_query

    async def _generate_sql_query(self, question: str) -> str:
        """Generate SQL query from natural language question.

        Args:
            question: User's natural language question

        Returns:
            SQL query string
        """
        messages = [
            Message("system", TEXT2SQL_SYSTEM_PROMPT),
            Message("user", f"Generate a SQL query to answer: {question}"),
        ]

        response = await self.llm_client.get_response(messages)

        # Clean up response (remove markdown, extra whitespace)
        sql_query = response.strip()
        sql_query = sql_query.replace("```sql", "").replace("```", "")
        return sql_query.strip()


    async def _generate_answer(self, question: str, query_results: str) -> str:
        """Generate natural language answer from query results.

        Args:
            question: Original user question
            query_results: Formatted query results

        Returns:
            Natural language answer
        """
        messages = [
            Message("system", ANSWER_SYSTEM_PROMPT),
            Message(
                "user",
                f"Question: {question}\n\nQuery Results:\n{query_results}\n\n"
                f"Please provide a clear answer to the question based on these results.",
            ),
        ]

        return await self.llm_client.get_response(messages)

