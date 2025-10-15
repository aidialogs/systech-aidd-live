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

    def add_message(self, user_id: int, chat_id: int, message: Message) -> None:
        """Add a message to the conversation context."""
        ...

    def get_context(self, user_id: int, chat_id: int) -> list[Message]:
        """Get conversation context for a user in a specific chat."""
        ...

    def clear_context(self, user_id: int, chat_id: int) -> None:
        """Clear conversation context for a user in a specific chat."""
        ...


class StatsCollectorProtocol(Protocol):
    """Protocol for stats collector implementations."""

    async def collect_stats(self, time_range: str = "7d") -> dict[str, Any]:
        """Collect statistics for the given time range."""
        ...
