"""Mock implementation of StatsCollector for frontend development."""

import math
import random
from datetime import UTC, datetime, timedelta

from src.protocols import ChartDataPoint, DashboardStats, MetricCard


class MockStatsCollector:
    """Mock stats collector with generated realistic data."""

    async def get_dashboard_stats(self) -> DashboardStats:
        """Generate mock dashboard statistics."""
        # Generate metric cards with realistic data
        total_users = self._generate_metric_card(
            title="Total Users",
            base_value=random.randint(800, 2000),
            description="Total registered users",
        )

        active_dialogs = self._generate_metric_card(
            title="Active Dialogs",
            base_value=random.randint(200, 800),
            description="Unique active conversations",
        )

        total_messages = self._generate_metric_card(
            title="Total Messages",
            base_value=random.randint(10000, 100000),
            description="All messages exchanged",
        )

        avg_message_length = self._generate_metric_card(
            title="Avg Message Length",
            base_value=random.randint(80, 200),
            description="Average characters per message",
        )

        # Generate chart data
        messages_chart_7d = self._generate_chart_data(days=7)
        messages_chart_30d = self._generate_chart_data(days=30)

        return DashboardStats(
            total_users=total_users,
            active_dialogs=active_dialogs,
            total_messages=total_messages,
            avg_message_length=avg_message_length,
            messages_chart_7d=messages_chart_7d,
            messages_chart_30d=messages_chart_30d,
        )

    def _generate_metric_card(self, title: str, base_value: int, description: str) -> MetricCard:
        """Generate a metric card with trend."""
        # Format value with thousands separator
        formatted_value = f"{base_value:,}"

        # Generate realistic trend (-30% to +30%)
        trend_value = random.uniform(-30, 30)
        trend_sign = "+" if trend_value >= 0 else ""
        trend = f"{trend_sign}{trend_value:.1f}%"

        return MetricCard(
            title=title,
            value=formatted_value,
            trend=trend,
            description=description,
        )

    def _generate_chart_data(self, days: int) -> list[ChartDataPoint]:
        """Generate chart data with wave pattern for realistic activity."""
        now = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
        data_points: list[ChartDataPoint] = []

        # Base value for messages per day
        base_value = random.randint(800, 2000)

        for i in range(days):
            # Calculate date (going backwards from today)
            date = now - timedelta(days=days - 1 - i)
            date_str = date.strftime("%Y-%m-%dT00:00:00Z")

            # Generate wave pattern with some randomness
            # Using sine wave for natural activity pattern
            wave = math.sin(i * 0.5) * 300  # Amplitude of 300
            random_noise = random.randint(-150, 150)
            value = int(base_value + wave + random_noise)

            # Ensure value is positive
            value = max(value, 100)

            data_points.append(ChartDataPoint(date=date_str, value=value))

        return data_points
