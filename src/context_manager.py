import logging

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.message import Message
from src.repository import MessageRepository


class ContextManager:
    """Manages conversation context for multiple users and chats with database persistence."""

    def __init__(self, session_maker: async_sessionmaker, max_context_messages: int) -> None:
        """Initialize context manager with session maker and max context size.

        Args:
            session_maker: SQLAlchemy async session maker
            max_context_messages: Maximum number of messages to keep in context
        """
        self.session_maker = session_maker
        self.max_context_messages = max_context_messages

    async def add_message(self, user_id: int, chat_id: int, message: Message) -> None:
        """Add a message to the conversation context (saves to database).

        Args:
            user_id: Telegram user_id
            chat_id: Telegram chat_id
            message: Message to add
        """
        async with self.session_maker() as session:
            repository = MessageRepository(session)

            # Save message to database
            await repository.add_message(
                user_id=user_id, chat_id=chat_id, role=message.role, content=message.content
            )
            await session.commit()

            logging.info(
                f"Message added to context: user_id={user_id} chat_id={chat_id} role={message.role}"
            )

        # Note: Context trimming is now handled by get_messages() with LIMIT
        # Full history is preserved in database

    async def get_context(self, user_id: int, chat_id: int) -> list[Message]:
        """Get conversation context for a user in a specific chat.

        Args:
            user_id: Telegram user_id
            chat_id: Telegram chat_id

        Returns:
            List of last N messages (with system prompt first)
        """
        async with self.session_maker() as session:
            repository = MessageRepository(session)

            # Get messages from database (limited by max_context_messages)
            orm_messages = await repository.get_messages(
                user_id=user_id, chat_id=chat_id, limit=self.max_context_messages
            )

            # Convert ORM messages to Message objects
            messages = [Message.from_orm(msg) for msg in orm_messages]

            logging.debug(
                f"Retrieved context: user_id={user_id} chat_id={chat_id} count={len(messages)}"
            )

            return messages

    async def clear_context(self, user_id: int, chat_id: int) -> None:
        """Clear conversation context for a user in a specific chat (soft delete).

        Args:
            user_id: Telegram user_id
            chat_id: Telegram chat_id
        """
        async with self.session_maker() as session:
            repository = MessageRepository(session)

            count = await repository.soft_delete_messages(user_id=user_id, chat_id=chat_id)
            await session.commit()

            if count > 0:
                logging.info(f"Context cleared: user_id={user_id} chat_id={chat_id} count={count}")
            else:
                logging.info(f"No context to clear for user_id={user_id} chat_id={chat_id}")
