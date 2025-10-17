"""Chat handler with normal and admin modes."""

import logging
import re

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.api.chat_schemas import ChatRequest, ChatResponse
from src.context_manager import ContextManager
from src.exceptions import LLMError
from src.llm_client import LLMClient
from src.message import Message

logger = logging.getLogger(__name__)

# Text2SQL system prompt
TEXT2SQL_PROMPT = """У тебя есть доступ к БД PostgreSQL с таблицами:

Таблица users:
- id (bigint, primary key) - ID пользователя Telegram
- created_at (timestamp) - дата создания
- is_deleted (boolean) - флаг удаления

Таблица messages:
- id (integer, primary key) - ID сообщения
- user_id (bigint, foreign key to users.id) - ID пользователя
- chat_id (bigint) - ID чата Telegram
- role (varchar) - роль: 'user', 'assistant', или 'system'
- content (text) - текст сообщения
- content_length (integer) - длина сообщения
- created_at (timestamp) - дата создания
- is_deleted (boolean) - флаг удаления

Вопрос пользователя: "{question}"

Сгенерируй SQL запрос (только SELECT) для ответа на этот вопрос.
Верни только SQL запрос без дополнительных объяснений, комментариев или markdown форматирования.
Используй ТОЛЬКО SELECT запросы. Не используй INSERT, UPDATE, DELETE, DROP и другие модифицирующие операции.
"""


class ChatHandler:
    """Handler for chat requests with normal and admin modes."""

    def __init__(
        self,
        llm_client: LLMClient,
        session_maker: async_sessionmaker,
        system_prompt: str,
        max_context_messages: int,
    ) -> None:
        """Initialize chat handler.

        Args:
            llm_client: LLM client for AI responses
            session_maker: Database session maker
            system_prompt: System prompt for normal mode
            max_context_messages: Maximum context messages to keep
        """
        self.llm_client = llm_client
        self.session_maker = session_maker
        self.system_prompt = system_prompt
        self.max_context = max_context_messages
        self.context_manager = ContextManager(session_maker, max_context_messages)

    async def handle_message(self, request: ChatRequest) -> ChatResponse:
        """Handle incoming chat message.

        Args:
            request: Chat request with message and mode

        Returns:
            Chat response with assistant message
        """
        logger.info(
            f"Handling chat message: user_id={request.user_id}, "
            f"chat_id={request.chat_id}, mode={request.mode}"
        )

        if request.mode == "admin":
            return await self._handle_admin_mode(request)
        return await self._handle_normal_mode(request)

    async def _handle_normal_mode(self, request: ChatRequest) -> ChatResponse:
        """Handle normal mode - regular LLM conversation.

        Args:
            request: Chat request

        Returns:
            Chat response with LLM message
        """
        try:
            # Get context
            context = await self.context_manager.get_context(request.user_id, request.chat_id)

            # Add system prompt if context is empty
            if not context:
                system_message = Message("system", self.system_prompt)
                await self.context_manager.add_message(
                    request.user_id, request.chat_id, system_message
                )

            # Add user message to context
            user_message = Message("user", request.message)
            await self.context_manager.add_message(request.user_id, request.chat_id, user_message)

            # Get updated context for LLM
            context = await self.context_manager.get_context(request.user_id, request.chat_id)

            logger.info(f"Sending to LLM: context_size={len(context)}")

            # Get response from LLM
            response = await self.llm_client.get_response(context)

            # Add assistant message to context
            assistant_message = Message("assistant", response)
            await self.context_manager.add_message(
                request.user_id, request.chat_id, assistant_message
            )

            logger.info("Normal mode response generated successfully")

            return ChatResponse(message=response, mode="normal")

        except LLMError as e:
            logger.error(f"LLM error in normal mode: {e!s}")
            error_msg = "Извините, не могу ответить прямо сейчас. Попробуйте чуть позже."
            return ChatResponse(message=error_msg, mode="normal")
        except Exception as e:
            logger.error(f"Unexpected error in normal mode: {e!s}", exc_info=True)
            error_msg = "Извините, произошла ошибка. Попробуйте еще раз."
            return ChatResponse(message=error_msg, mode="normal")

    async def _handle_admin_mode(self, request: ChatRequest) -> ChatResponse:
        """Handle admin mode - text2sql pipeline.

        Args:
            request: Chat request

        Returns:
            Chat response with data analysis result and SQL query
        """
        try:
            # Step 1: Generate SQL query using LLM
            text2sql_prompt = TEXT2SQL_PROMPT.format(question=request.message)
            sql_messages = [Message("user", text2sql_prompt)]

            logger.info("Generating SQL query from user question")
            sql_query = await self.llm_client.get_response(sql_messages)

            # Clean SQL query - remove markdown formatting and extra whitespace
            sql_query = self._clean_sql_query(sql_query)

            logger.info(f"Generated SQL: {sql_query}")

            # Step 2: Validate SQL (basic safety check)
            if not self._is_safe_sql(sql_query):
                logger.warning(f"Unsafe SQL query detected: {sql_query}")
                return ChatResponse(
                    message="Извините, не могу выполнить этот запрос. Разрешены только SELECT запросы.",
                    mode="admin",
                    sql_query=sql_query,
                )

            # Step 3: Execute SQL query
            logger.info("Executing SQL query")
            query_result = await self._execute_sql(sql_query)

            # Step 4: Send results to LLM for natural language response
            result_prompt = f"""Пользователь задал вопрос: "{request.message}"

Я выполнил SQL запрос и получил следующие результаты:
{query_result}

Сформулируй понятный ответ на вопрос пользователя на основе этих данных.
Ответ должен быть кратким и информативным."""

            result_messages = [Message("user", result_prompt)]
            logger.info("Generating natural language response from query results")
            final_response = await self.llm_client.get_response(result_messages)

            logger.info("Admin mode response generated successfully")

            return ChatResponse(message=final_response, mode="admin", sql_query=sql_query)

        except LLMError as e:
            logger.error(f"LLM error in admin mode: {e!s}")
            error_msg = "Извините, не могу обработать запрос. Попробуйте переформулировать вопрос."
            return ChatResponse(message=error_msg, mode="admin")
        except Exception as e:
            logger.error(f"Error in admin mode: {e!s}")
            error_msg = f"Ошибка при выполнении запроса: {e!s}"
            return ChatResponse(message=error_msg, mode="admin")

    def _clean_sql_query(self, sql: str) -> str:
        """Clean SQL query by removing markdown and extra whitespace.

        Args:
            sql: Raw SQL query from LLM

        Returns:
            Cleaned SQL query
        """
        # Remove markdown code blocks
        sql = re.sub(r"```sql\n?", "", sql)
        sql = re.sub(r"```\n?", "", sql)

        # Remove extra whitespace
        sql = sql.strip()

        return sql

    def _is_safe_sql(self, sql: str) -> bool:
        """Check if SQL query is safe (only SELECT).

        Args:
            sql: SQL query to check

        Returns:
            True if safe, False otherwise
        """
        sql_upper = sql.upper().strip()

        # Must start with SELECT
        if not sql_upper.startswith("SELECT"):
            return False

        # Must not contain dangerous keywords as separate words
        dangerous_keywords = [
            "INSERT",
            "UPDATE",
            "DELETE",
            "DROP",
            "CREATE",
            "ALTER",
            "TRUNCATE",
            "EXEC",
            "EXECUTE",
        ]

        # Check for dangerous keywords as whole words (with word boundaries)
        import re

        for keyword in dangerous_keywords:
            # Use word boundary to match whole words only
            if re.search(r"\b" + keyword + r"\b", sql_upper):
                return False

        return True

    async def _execute_sql(self, sql: str) -> str:
        """Execute SQL query and return results as string.

        Args:
            sql: SQL query to execute

        Returns:
            Query results as formatted string
        """
        async with self.session_maker() as session:
            result = await session.execute(text(sql))

            # Fetch all rows
            rows = result.fetchall()

            if not rows:
                return "Запрос не вернул результатов."

            # Format results
            # Get column names
            columns = list(result.keys())

            # Build result string
            result_lines = [f"Колонки: {', '.join(columns)}", ""]

            # Add rows (limit to 100 rows for safety)
            max_rows = 100
            for i, row in enumerate(rows[:max_rows]):
                row_data = ", ".join(str(value) for value in row)
                result_lines.append(f"Строка {i + 1}: {row_data}")

            if len(rows) > max_rows:
                result_lines.append(f"\n... и еще {len(rows) - max_rows} строк")

            return "\n".join(result_lines)
