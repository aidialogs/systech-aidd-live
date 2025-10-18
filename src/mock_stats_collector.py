"""Mock implementation of statistics collector with fixed data."""

from datetime import UTC, datetime, timedelta
from typing import Any


class MockStatCollector:
    """Mock implementation of statistics collector with fixed data.

    This class returns predefined statistics data for testing and frontend development.
    Data is fixed and does not change between calls.
    """

    async def get_stats(self, period_days: int) -> dict[str, Any]:
        """Return fixed mock statistics data.

        Args:
            period_days: Number of days (7 or 30)

        Returns:
            Dictionary with metrics and timeline data
        """
        if period_days == 7:
            return self._get_stats_7d()
        if period_days == 30:
            return self._get_stats_30d()
        # Default to 7 days
        return self._get_stats_7d()

    def _get_stats_7d(self) -> dict[str, Any]:
        """Get statistics for last 7 days."""
        # Generate dates for last 7 days
        end_date = datetime.now(tz=UTC).date()
        dates = [(end_date - timedelta(days=i)) for i in range(6, -1, -1)]

        return {
            "metrics": {
                "total_users": {"value": 1250, "trend": 12.5},
                "total_chats": {"value": 1089, "trend": 8.3},
                "total_messages": {"value": 45678, "trend": 15.7},
                "avg_message_length": {"value": 142, "trend": 3.2},
            },
            "timeline": [
                {"date": dates[0].isoformat(), "messages": 6234},
                {"date": dates[1].isoformat(), "messages": 6521},
                {"date": dates[2].isoformat(), "messages": 6187},
                {"date": dates[3].isoformat(), "messages": 6789},
                {"date": dates[4].isoformat(), "messages": 6432},
                {"date": dates[5].isoformat(), "messages": 6891},
                {"date": dates[6].isoformat(), "messages": 6624},
            ],
        }

    def _get_stats_30d(self) -> dict[str, Any]:
        """Get statistics for last 30 days."""
        # Generate dates for last 30 days
        end_date = datetime.now(tz=UTC).date()
        dates = [(end_date - timedelta(days=i)) for i in range(29, -1, -1)]

        return {
            "metrics": {
                "total_users": {"value": 11250, "trend": 12.5},
                "total_chats": {"value": 11089, "trend": -5.2},
                "total_messages": {"value": 145678, "trend": 8.3},
                "avg_message_length": {"value": 142, "trend": 3.1},
            },
            "timeline": [
                {"date": dates[0].isoformat(), "messages": 1234},
                {"date": dates[1].isoformat(), "messages": 1345},
                {"date": dates[2].isoformat(), "messages": 1289},
                {"date": dates[3].isoformat(), "messages": 1456},
                {"date": dates[4].isoformat(), "messages": 1523},
                {"date": dates[5].isoformat(), "messages": 1398},
                {"date": dates[6].isoformat(), "messages": 1487},
                {"date": dates[7].isoformat(), "messages": 1654},
                {"date": dates[8].isoformat(), "messages": 1589},
                {"date": dates[9].isoformat(), "messages": 1723},
                {"date": dates[10].isoformat(), "messages": 1812},
                {"date": dates[11].isoformat(), "messages": 1698},
                {"date": dates[12].isoformat(), "messages": 1765},
                {"date": dates[13].isoformat(), "messages": 1889},
                {"date": dates[14].isoformat(), "messages": 1834},
                {"date": dates[15].isoformat(), "messages": 1956},
                {"date": dates[16].isoformat(), "messages": 2087},
                {"date": dates[17].isoformat(), "messages": 1998},
                {"date": dates[18].isoformat(), "messages": 2123},
                {"date": dates[19].isoformat(), "messages": 2234},
                {"date": dates[20].isoformat(), "messages": 2156},
                {"date": dates[21].isoformat(), "messages": 2289},
                {"date": dates[22].isoformat(), "messages": 2378},
                {"date": dates[23].isoformat(), "messages": 2298},
                {"date": dates[24].isoformat(), "messages": 2412},
                {"date": dates[25].isoformat(), "messages": 2534},
                {"date": dates[26].isoformat(), "messages": 2456},
                {"date": dates[27].isoformat(), "messages": 2598},
                {"date": dates[28].isoformat(), "messages": 2687},
                {"date": dates[29].isoformat(), "messages": 2789},
            ],
        }
