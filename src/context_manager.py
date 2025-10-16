import logging

from src.database import DatabaseRepository
from src.message import Message


class ContextManager:
    """Manages conversation context for multiple users and chats using database storage."""

    def __init__(self, db_repository: DatabaseRepository, max_context_messages: int) -> None:
        """Initialize ContextManager with database repository.

        Args:
            db_repository: DatabaseRepository for persistent storage
            max_context_messages: Maximum number of messages to keep in context
        """
        self.db_repository = db_repository
        self.max_context_messages = max_context_messages

    async def add_message(self, user_id: int, chat_id: int, message: Message) -> None:
        """Add a message to the conversation context.

        Args:
            user_id: Telegram user ID
            chat_id: Telegram chat ID
            message: Message to add
        """
        # Save message to database
        await self.db_repository.save_message(user_id, chat_id, message.role, message.content)

        # Get current context size to check if trimming is needed
        current_context = await self.db_repository.get_messages(
            user_id, chat_id, self.max_context_messages + 1
        )

        logging.info(
            f"Message added to context: user_id={user_id} chat_id={chat_id} "
            f"role={message.role} context_size={len(current_context)}"
        )

        # Trim context if exceeds max_context_messages (keep system prompt)
        if len(current_context) > self.max_context_messages:
            await self._trim_context(user_id, chat_id, current_context)

    async def _trim_context(
        self, user_id: int, chat_id: int, messages: list[Message]
    ) -> None:
        """Trim context to keep only system prompt and recent messages.

        Args:
            user_id: Telegram user ID
            chat_id: Telegram chat ID
            messages: Current list of messages
        """
        old_size = len(messages)

        # Delete all messages for this user/chat
        await self.db_repository.delete_messages(user_id, chat_id)

        # Preserve system prompt (first message) and keep most recent messages
        system_msg = messages[0]
        recent_messages = messages[-(self.max_context_messages - 1) :]

        # Re-save system prompt and recent messages
        await self.db_repository.save_message(
            user_id, chat_id, system_msg.role, system_msg.content
        )
        for msg in recent_messages:
            await self.db_repository.save_message(user_id, chat_id, msg.role, msg.content)

        logging.info(
            f"Context trimmed: user_id={user_id} chat_id={chat_id} "
            f"old_size={old_size} new_size={self.max_context_messages}"
        )

    async def get_context(self, user_id: int, chat_id: int) -> list[Message]:
        """Get conversation context for a user in a specific chat.

        Args:
            user_id: Telegram user ID
            chat_id: Telegram chat ID

        Returns:
            List of Message objects from database
        """
        return await self.db_repository.get_messages(user_id, chat_id, self.max_context_messages)

    async def clear_context(self, user_id: int, chat_id: int) -> None:
        """Clear conversation context for a user in a specific chat.

        Args:
            user_id: Telegram user ID
            chat_id: Telegram chat ID
        """
        await self.db_repository.delete_messages(user_id, chat_id)
        logging.info(f"Context cleared for user_id={user_id} chat_id={chat_id}")
