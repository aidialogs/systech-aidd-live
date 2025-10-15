"""Mock stats collector with hardcoded demo data."""

from datetime import UTC, datetime, timedelta
from typing import Any


class MockStatsCollector:
    """Mock implementation with hardcoded demo data."""

    async def collect_stats(self, time_range: str = "7d") -> dict[str, Any]:
        """Return mock statistics with beautiful demo data."""

        # Overview metrics (hardcoded)
        overview = {
            "total_users": {"value": 250, "trend": 12.5, "trend_direction": "up"},
            "total_conversations": {"value": 334, "trend": -5.2, "trend_direction": "down"},
            "total_messages": {"value": 13420, "trend": 8.3, "trend_direction": "up"},
            "avg_conversation_length": {"value": 114.6, "trend": 2.1, "trend_direction": "up"},
        }

        # Message activity data points (generated based on time_range)
        days = 7 if time_range == "7d" else 30
        now = datetime.now(UTC)

        # Hardcoded message counts for variety
        message_counts = [145, 52, 38, 61, 49, 55, 43]  # для 7d
        if days == 30:
            message_counts = [
                145,
                52,
                38,
                61,
                49,
                55,
                43,
                50,
                48,
                56,
                42,
                58,
                47,
                53,
                39,
                62,
                44,
                57,
                51,
                46,
                54,
                41,
                59,
                48,
                152,
                43,
                160,
                49,
                155,
                147,
            ]

        data_points = []
        for i in range(days):
            timestamp = (now - timedelta(days=days - 1 - i)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            data_points.append(
                {"timestamp": timestamp.isoformat(), "message_count": message_counts[i]}
            )

        return {
            "overview": overview,
            "message_activity": {"time_range": time_range, "data_points": data_points},
        }
