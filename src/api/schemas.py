"""Pydantic schemas for API responses."""

from pydantic import BaseModel, Field


class Overview(BaseModel):
    """Overview statistics."""

    total_messages: int = Field(..., description="Total number of messages")
    total_users: int = Field(..., description="Total number of users")
    active_chats: int = Field(..., description="Number of active chats")
    avg_message_length: int = Field(..., description="Average message length in characters")


class MessagesByRole(BaseModel):
    """Messages grouped by role."""

    user: int = Field(..., description="Number of user messages")
    assistant: int = Field(..., description="Number of assistant messages")
    system: int = Field(..., description="Number of system messages")


class TimeSeriesPoint(BaseModel):
    """Single point in time series."""

    date: str = Field(..., description="Date or datetime (ISO format)")
    count: int = Field(..., description="Number of messages")


class TopMetrics(BaseModel):
    """Top-level metrics."""

    most_active_users: int = Field(..., description="Number of most active users")
    messages_today: int = Field(..., description="Messages sent today")
    messages_this_week: int = Field(..., description="Messages sent this week")
    messages_this_month: int = Field(..., description="Messages sent this month")


class Statistics(BaseModel):
    """Complete statistics response."""

    period: str = Field(..., description="Selected time period (day|week|month|all)")
    overview: Overview = Field(..., description="Overview statistics")
    messages_by_role: MessagesByRole = Field(..., description="Messages grouped by role")
    messages_over_time: list[TimeSeriesPoint] = Field(..., description="Time series data")
    top_metrics: TopMetrics = Field(..., description="Top-level metrics")
