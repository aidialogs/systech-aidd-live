"""Mock implementation of statistics collector."""

import random
from datetime import UTC, datetime, timedelta

from src.api.schemas import (
    MessagesByRole,
    Overview,
    Statistics,
    TimeSeriesPoint,
    TopMetrics,
)


class MockStatCollector:
    """Mock statistics collector with generated data."""

    async def get_statistics(self, period: str = "month") -> Statistics:
        """Generate mock statistics for specified period.

        Args:
            period: Time period (day|week|month|all)

        Returns:
            Statistics object with mock data
        """
        # Generate base numbers
        total_messages = random.randint(10000, 20000)
        total_users = random.randint(200, 500)
        active_chats = random.randint(150, total_users)

        # Calculate role distribution
        user_messages = int(total_messages * random.uniform(0.50, 0.58))
        assistant_messages = int(total_messages * random.uniform(0.38, 0.45))
        system_messages = total_messages - user_messages - assistant_messages

        # Generate time series based on period
        time_series = self._generate_time_series(period)

        # Generate top metrics
        messages_today = random.randint(100, 300)
        messages_this_week = random.randint(700, 1500)
        messages_this_month = random.randint(3000, 6000)

        return Statistics(
            period=period,
            overview=Overview(
                total_messages=total_messages,
                total_users=total_users,
                active_chats=active_chats,
                avg_message_length=random.randint(50, 150),
            ),
            messages_by_role=MessagesByRole(
                user=user_messages,
                assistant=assistant_messages,
                system=system_messages,
            ),
            messages_over_time=time_series,
            top_metrics=TopMetrics(
                most_active_users=random.randint(3, 10),
                messages_today=messages_today,
                messages_this_week=messages_this_week,
                messages_this_month=messages_this_month,
            ),
        )

    def _generate_time_series(self, period: str) -> list[TimeSeriesPoint]:
        """Generate time series data based on period.

        Args:
            period: Time period (day|week|month|all)

        Returns:
            List of time series points
        """
        now = datetime.now(UTC)
        points: list[TimeSeriesPoint] = []

        if period == "day":
            # 24 hours (by hour)
            for i in range(24):
                hour_time = now - timedelta(hours=23 - i)
                points.append(
                    TimeSeriesPoint(
                        date=hour_time.strftime("%Y-%m-%d %H:00"),
                        count=random.randint(20, 100),
                    )
                )
        elif period == "week":
            # 7 days
            for i in range(7):
                day_time = now - timedelta(days=6 - i)
                points.append(
                    TimeSeriesPoint(
                        date=day_time.strftime("%Y-%m-%d"),
                        count=random.randint(100, 300),
                    )
                )
        elif period == "month":
            # 30 days
            for i in range(30):
                day_time = now - timedelta(days=29 - i)
                points.append(
                    TimeSeriesPoint(
                        date=day_time.strftime("%Y-%m-%d"),
                        count=random.randint(100, 500),
                    )
                )
        elif period == "all":
            # 12 months
            for i in range(12):
                month_time = now - timedelta(days=30 * (11 - i))
                points.append(
                    TimeSeriesPoint(
                        date=month_time.strftime("%Y-%m"),
                        count=random.randint(1000, 3000),
                    )
                )

        return points
