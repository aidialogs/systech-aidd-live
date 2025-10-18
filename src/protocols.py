"""Protocol interfaces for dependency injection."""

from typing import Any, Protocol

from src.message import Message


class LLMClientProtocol(Protocol):
    """Protocol for LLM client implementations."""

    async def get_response(self, messages: list[Message]) -> str:
        """Get response from LLM for given messages."""
        ...


class ContextManagerProtocol(Protocol):
    """Protocol for context manager implementations."""

    async def add_message(self, user_id: int, chat_id: int, message: Message) -> None:
        """Add a message to the conversation context."""
        ...

    async def get_context(self, user_id: int, chat_id: int) -> list[Message]:
        """Get conversation context for a user in a specific chat."""
        ...

    async def clear_context(self, user_id: int, chat_id: int) -> None:
        """Clear conversation context for a user in a specific chat."""
        ...


class StatCollectorProtocol(Protocol):
    """Protocol for statistics collection."""

    async def get_stats(self, period_days: int) -> dict[str, Any]:
        """Get statistics for specified period.

        Args:
            period_days: Number of days to collect statistics for (7 or 30)

        Returns:
            Dictionary with metrics and timeline data
        """
        ...
