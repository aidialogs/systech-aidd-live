"""Real StatCollector implementation with database queries."""

import logging
from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.api.protocols import StatCollectorProtocol
from src.api.schemas import MessagesByRole, Overview, Statistics, TimeSeriesPoint, TopMetrics
from src.models import Message

logger = logging.getLogger(__name__)


class RealStatCollector(StatCollectorProtocol):
    """Real statistics collector using database queries."""

    def __init__(self, session_maker: async_sessionmaker) -> None:
        """Initialize with database session maker.

        Args:
            session_maker: SQLAlchemy async session maker
        """
        self.session_maker = session_maker

    def _get_date_range(self, period: str) -> datetime | None:
        """Get start date for the given period.

        Args:
            period: Time period (day, week, month, all)

        Returns:
            Start datetime for the period, or None for 'all'
        """
        now = datetime.now()

        if period == "day":
            return now - timedelta(days=1)
        if period == "week":
            return now - timedelta(weeks=1)
        if period == "month":
            return now - timedelta(days=30)
        # all
        return None

    async def get_statistics(self, period: str) -> Statistics:
        """Get statistics for specified period from database.

        Args:
            period: Time period (day, week, month, all)

        Returns:
            Statistics object with data from database
        """
        logger.info(f"Collecting real statistics for period: {period}")

        async with self.session_maker() as session:
            start_date = self._get_date_range(period)

            # Base filter for non-deleted messages
            base_filter = [Message.is_deleted == False]  # noqa: E712
            if start_date:
                base_filter.append(Message.created_at >= start_date)

            # Overview statistics
            # Total messages
            stmt = select(func.count(Message.id)).where(*base_filter)
            result = await session.execute(stmt)
            total_messages = result.scalar() or 0

            # Total users
            stmt = select(func.count(func.distinct(Message.user_id))).where(*base_filter)
            result = await session.execute(stmt)
            total_users = result.scalar() or 0

            # Active chats
            stmt = select(func.count(func.distinct(Message.chat_id))).where(*base_filter)
            result = await session.execute(stmt)
            active_chats = result.scalar() or 0

            # Average message length
            stmt = select(func.avg(Message.content_length)).where(*base_filter)
            result = await session.execute(stmt)
            avg_length = result.scalar()
            avg_message_length = int(avg_length) if avg_length else 0

            overview = Overview(
                total_messages=total_messages,
                total_users=total_users,
                active_chats=active_chats,
                avg_message_length=avg_message_length,
            )

            # Messages by role
            stmt = (
                select(Message.role, func.count(Message.id))
                .where(*base_filter)
                .group_by(Message.role)
            )
            result = await session.execute(stmt)
            role_counts = {role: count for role, count in result.all()}

            messages_by_role = MessagesByRole(
                user=role_counts.get("user", 0),
                assistant=role_counts.get("assistant", 0),
                system=role_counts.get("system", 0),
            )

            # Messages over time (by date)
            stmt = (
                select(
                    func.date(Message.created_at).label("date"),
                    func.count(Message.id).label("count"),
                )
                .where(*base_filter)
                .group_by(func.date(Message.created_at))
                .order_by(func.date(Message.created_at))
            )
            result = await session.execute(stmt)
            time_series_data = [
                TimeSeriesPoint(date=str(date), count=count) for date, count in result.all()
            ]

            # Top metrics
            # Messages today
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            stmt = select(func.count(Message.id)).where(
                Message.is_deleted == False,  # noqa: E712
                Message.created_at >= today_start,
            )
            result = await session.execute(stmt)
            messages_today = result.scalar() or 0

            # Messages this week
            week_start = datetime.now() - timedelta(days=7)
            stmt = select(func.count(Message.id)).where(
                Message.is_deleted == False,  # noqa: E712
                Message.created_at >= week_start,
            )
            result = await session.execute(stmt)
            messages_this_week = result.scalar() or 0

            # Messages this month
            month_start = datetime.now() - timedelta(days=30)
            stmt = select(func.count(Message.id)).where(
                Message.is_deleted == False,  # noqa: E712
                Message.created_at >= month_start,
            )
            result = await session.execute(stmt)
            messages_this_month = result.scalar() or 0

            # Most active users (count of distinct users with >10 messages)
            stmt = (
                select(func.count(func.distinct(Message.user_id)))
                .where(*base_filter)
                .group_by(Message.user_id)
                .having(func.count(Message.id) > 10)
            )
            result = await session.execute(stmt)
            most_active_users = len(result.all())

            top_metrics = TopMetrics(
                most_active_users=most_active_users,
                messages_today=messages_today,
                messages_this_week=messages_this_week,
                messages_this_month=messages_this_month,
            )

            logger.info(
                f"Statistics collected: {total_messages} messages, {total_users} users, {active_chats} chats"
            )

            return Statistics(
                period=period,
                overview=overview,
                messages_by_role=messages_by_role,
                messages_over_time=time_series_data,
                top_metrics=top_metrics,
            )


