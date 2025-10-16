"""Database repository for message storage."""

import logging
from typing import Any

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from src.message import Message


class DatabaseRepository:
    """Repository for database operations with messages."""

    def __init__(self, pool: AsyncConnectionPool) -> None:
        """Initialize repository with connection pool.

        Args:
            pool: AsyncConnectionPool for database connections
        """
        self.pool = pool

    async def save_message(
        self, user_id: int, chat_id: int, role: str, content: str
    ) -> None:
        """Save a message to the database.

        Args:
            user_id: Telegram user ID
            chat_id: Telegram chat ID
            role: Message role (system, user, assistant)
            content: Message content
        """
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO messages (user_id, chat_id, role, content)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (user_id, chat_id, role, content),
                )
                await conn.commit()
                logging.info(
                    f"Message saved to DB: user_id={user_id} chat_id={chat_id} role={role}"
                )

    async def get_messages(
        self, user_id: int, chat_id: int, limit: int
    ) -> list[Message]:
        """Retrieve messages for a user in a chat.

        Args:
            user_id: Telegram user ID
            chat_id: Telegram chat ID
            limit: Maximum number of messages to retrieve

        Returns:
            List of Message objects ordered by creation time (oldest first)
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(
                    """
                    SELECT role, content
                    FROM messages
                    WHERE user_id = %s AND chat_id = %s
                    ORDER BY created_at ASC
                    LIMIT %s
                    """,
                    (user_id, chat_id, limit),
                )
                rows: list[dict[str, Any]] = await cur.fetchall()
                messages = [Message(role=row["role"], content=row["content"]) for row in rows]
                logging.info(
                    f"Retrieved {len(messages)} messages from DB: "
                    f"user_id={user_id} chat_id={chat_id}"
                )
                return messages

    async def delete_messages(self, user_id: int, chat_id: int) -> None:
        """Delete all messages for a user in a chat.

        Args:
            user_id: Telegram user ID
            chat_id: Telegram chat ID
        """
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    DELETE FROM messages
                    WHERE user_id = %s AND chat_id = %s
                    """,
                    (user_id, chat_id),
                )
                deleted_count = cur.rowcount
                await conn.commit()
                logging.info(
                    f"Deleted {deleted_count} messages from DB: "
                    f"user_id={user_id} chat_id={chat_id}"
                )


async def create_connection_pool(database_url: str) -> AsyncConnectionPool:
    """Create and open a connection pool.

    Args:
        database_url: PostgreSQL connection string

    Returns:
        Opened AsyncConnectionPool ready for use
    """
    pool = AsyncConnectionPool(
        conninfo=database_url,
        min_size=2,
        max_size=10,
        timeout=30.0,
        open=False,  # Don't open in constructor (deprecated)
    )
    await pool.open()
    logging.info("Database connection pool created and opened")
    return pool

