"""FastAPI server for bot statistics."""

import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Stats API", version="0.1.0")

# CORS для localhost:3000 (Next.js dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Log all requests with timing."""
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    logging.info(f"API request: {request.method} {request.url.path} - {duration:.0f}ms")
    return response


@app.get("/api/stats")
async def get_stats(
    request: Request, time_range: str = Query("7d", pattern="^(7d|30d)$")
) -> dict[str, Any]:
    """Get bot statistics for the specified time range."""
    stats_collector = request.app.state.stats_collector
    stats: dict[str, Any] = await stats_collector.collect_stats(time_range)
    logging.info(
        f"Stats collected: time_range={time_range}, "
        f"data_points={len(stats['message_activity']['data_points'])}"
    )
    return stats


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "stats-api"}
