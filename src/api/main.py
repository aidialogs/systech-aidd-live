"""FastAPI application for statistics API."""

from enum import Enum

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from src.mock_stats_collector import MockStatCollector


class Period(str, Enum):
    """Time period for statistics."""

    SEVEN_DAYS = "7d"
    THIRTY_DAYS = "30d"


# Create FastAPI application
app = FastAPI(
    title="Systech AIDD Stats API",
    description="API для получения статистики по диалогам с Telegram-ботом",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize statistics collector
stats_collector = MockStatCollector()


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint with API information."""
    return {
        "message": "Systech AIDD Stats API",
        "version": "1.0.0",
        "docs": "/docs",
        "stats_endpoint": "/api/stats",
    }


@app.get("/api/stats")
async def get_stats(period: Period = Query(Period.SEVEN_DAYS, description="Период статистики")):
    """Получить статистику за указанный период.

    Args:
        period: Период для статистики (7d или 30d)

    Returns:
        Статистика с метриками и временным рядом

    Examples:
        - GET /api/stats?period=7d  - статистика за последние 7 дней
        - GET /api/stats?period=30d - статистика за последние 30 дней
    """
    period_days = 7 if period == Period.SEVEN_DAYS else 30
    return await stats_collector.get_stats(period_days)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}

