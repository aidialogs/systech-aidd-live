"""Protocol interfaces for API components."""

from typing import Protocol

from src.api.schemas import Statistics


class StatCollectorProtocol(Protocol):
    """Protocol for statistics collector implementations."""

    async def get_statistics(self, period: str = "month") -> Statistics:
        """Get dashboard statistics for specified period.

        Args:
            period: Time period (day|week|month|all)

        Returns:
            Statistics object with complete dashboard data
        """
        ...
