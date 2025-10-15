"""Entry point for the API server."""

import asyncio
import logging
import os

import uvicorn
from dotenv import load_dotenv

from src.api_server import app
from src.config import Config
from src.mock_stats_collector import MockStatsCollector


async def main() -> None:
    """Main entry point for the API server."""
    load_dotenv()
    config = Config.from_env()

    # Setup logging (same as bot)
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
    )

    # Create mock stats collector
    stats_collector = MockStatsCollector()

    # Attach to app state
    app.state.stats_collector = stats_collector

    logging.info(f"API server starting on {config.api_host}:{config.api_port}")

    # Run uvicorn
    config_uvicorn = uvicorn.Config(
        app, host=config.api_host, port=config.api_port, log_level="info"
    )
    server = uvicorn.Server(config_uvicorn)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
