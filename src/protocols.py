"""Protocol interfaces for dependency injection."""

from dataclasses import dataclass
from typing import Protocol

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


@dataclass
class MetricCard:
    """Metric card for dashboard."""

    title: str
    value: str
    trend: str  # "+12.5%", "-20%", "+4.5%"
    description: str


@dataclass
class ChartDataPoint:
    """Data point for chart."""

    date: str  # ISO 8601 UTC format: "2025-01-05T00:00:00Z"
    value: int


@dataclass
class DashboardStats:
    """Complete dashboard statistics."""

    total_users: MetricCard
    active_dialogs: MetricCard
    total_messages: MetricCard
    avg_message_length: MetricCard
    messages_chart_7d: list[ChartDataPoint]  # 7 points
    messages_chart_30d: list[ChartDataPoint]  # 30 points


class StatsCollectorProtocol(Protocol):
    """Protocol for stats collection."""

    async def get_dashboard_stats(self) -> DashboardStats:
        """Get dashboard statistics."""
        ...
