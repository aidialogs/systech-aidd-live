"""FastAPI server for stats API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.mock_stats_collector import MockStatsCollector

app = FastAPI(
    title="AIDD Stats API",
    version="1.0.0",
    description="Statistics API for AI-driven Dialog Dashboard",
)

# CORS для локальной разработки frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "AIDD Stats API",
        "docs": "/docs",
        "stats": "/api/stats",
    }


@app.get("/api/stats")
async def get_stats() -> dict[str, dict[str, str] | list[dict[str, str | int]]]:
    """Get dashboard statistics.

    Returns mock data for frontend development.
    """
    collector = MockStatsCollector()
    stats = await collector.get_dashboard_stats()

    # Convert dataclasses to dict for JSON serialization
    return {
        "total_users": {
            "title": stats.total_users.title,
            "value": stats.total_users.value,
            "trend": stats.total_users.trend,
            "description": stats.total_users.description,
        },
        "active_dialogs": {
            "title": stats.active_dialogs.title,
            "value": stats.active_dialogs.value,
            "trend": stats.active_dialogs.trend,
            "description": stats.active_dialogs.description,
        },
        "total_messages": {
            "title": stats.total_messages.title,
            "value": stats.total_messages.value,
            "trend": stats.total_messages.trend,
            "description": stats.total_messages.description,
        },
        "avg_message_length": {
            "title": stats.avg_message_length.title,
            "value": stats.avg_message_length.value,
            "trend": stats.avg_message_length.trend,
            "description": stats.avg_message_length.description,
        },
        "messages_chart_7d": [
            {"date": point.date, "value": point.value} for point in stats.messages_chart_7d
        ],
        "messages_chart_30d": [
            {"date": point.date, "value": point.value} for point in stats.messages_chart_30d
        ],
    }
