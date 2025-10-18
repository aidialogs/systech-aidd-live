"""Repository pattern for database operations."""

import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src import models

logger = logging.getLogger(__name__)


class MessageRepository:
    """Repository for Message and User operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session."""
        self.session = session

    async def ensure_user(self, user_id: int) -> models.User:
        """Ensure user exists in database, create if not.

        Args:
            user_id: Telegram user_id

        Returns:
            User model instance
        """
        # Check if user exists
        stmt = select(models.User).where(models.User.id == user_id, ~models.User.is_deleted)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            logger.debug(f"User {user_id} already exists")
            return user

        # Create new user
        user = models.User(id=user_id)
        self.session.add(user)
        await self.session.flush()
        logger.info(f"Created new user: {user_id}")
        return user

    async def add_message(
        self, user_id: int, chat_id: int, role: str, content: str
    ) -> models.Message:
        """Add new message to database.

        Args:
            user_id: Telegram user_id
            chat_id: Telegram chat_id
            role: Message role (system/user/assistant)
            content: Message content

        Returns:
            Created Message model instance
        """
        # Ensure user exists
        await self.ensure_user(user_id)

        # Create message
        message = models.Message(
            user_id=user_id,
            chat_id=chat_id,
            role=role,
            content=content,
            content_length=len(content),
        )
        self.session.add(message)
        await self.session.flush()
        logger.debug(
            f"Added message: user_id={user_id} chat_id={chat_id} role={role} length={len(content)}"
        )
        return message

    async def get_messages(self, user_id: int, chat_id: int, limit: int) -> list[models.Message]:
        """Get last N messages for context.

        System prompt is always included first (not counted in limit).

        Args:
            user_id: Telegram user_id
            chat_id: Telegram chat_id
            limit: Maximum number of messages to return

        Returns:
            List of Message instances (chronologically ordered)
        """
        # 1. Get system prompt (first message with role='system')
        stmt_system = (
            select(models.Message)
            .where(
                models.Message.user_id == user_id,
                models.Message.chat_id == chat_id,
                models.Message.role == "system",
                ~models.Message.is_deleted,
            )
            .order_by(models.Message.created_at.asc())
            .limit(1)
        )
        result = await self.session.execute(stmt_system)
        system_msg = result.scalar_one_or_none()

        # 2. Get last (limit - 1) non-system messages
        messages_limit = limit - 1 if system_msg else limit
        stmt_messages = (
            select(models.Message)
            .where(
                models.Message.user_id == user_id,
                models.Message.chat_id == chat_id,
                models.Message.role != "system",
                ~models.Message.is_deleted,
            )
            .order_by(models.Message.created_at.desc())
            .limit(messages_limit)
        )
        result = await self.session.execute(stmt_messages)
        messages = list(reversed(result.scalars().all()))

        # 3. Return: [system_prompt] + other messages
        if system_msg:
            return [system_msg, *messages]
        return messages

    async def soft_delete_messages(self, user_id: int, chat_id: int) -> int:
        """Soft delete all messages for user in specific chat.

        Args:
            user_id: Telegram user_id
            chat_id: Telegram chat_id

        Returns:
            Number of messages marked as deleted
        """
        stmt = (
            update(models.Message)
            .where(
                models.Message.user_id == user_id,
                models.Message.chat_id == chat_id,
                ~models.Message.is_deleted,
            )
            .values(is_deleted=True)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()

        count = result.rowcount or 0  # type: ignore[attr-defined]
        logger.info(f"Soft deleted {count} messages for user_id={user_id} chat_id={chat_id}")
        return count
