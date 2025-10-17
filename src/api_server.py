"""API server entrypoint."""

import logging

import uvicorn
from dotenv import load_dotenv

from src import database
from src.api.chat_handler import ChatHandler
from src.api.main import create_app
from src.api.stat_collector_mock import MockStatCollector
from src.api.stat_collector_real import RealStatCollector
from src.config import Config
from src.llm_client import LLMClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Run API server."""
    # Load environment variables
    load_dotenv()

    # Load configuration
    try:
        config = Config.from_env()
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise

    # Initialize database (needed for both Real and chat)
    database.init_database(config.database_url, config.database_echo)
    logger.info("Database initialized")

    # Initialize StatCollector based on mode
    if config.stat_collector_mode == "mock":
        logger.info("Using MockStatCollector")
        stat_collector = MockStatCollector()
    elif config.stat_collector_mode == "real":
        logger.info("Using RealStatCollector")
        stat_collector = RealStatCollector(database.async_session_maker)
    else:
        logger.error(f"Unknown stat_collector_mode: {config.stat_collector_mode}")
        raise ValueError(f"Invalid STAT_COLLECTOR_MODE: {config.stat_collector_mode}")

    # Initialize LLM client for chat
    llm_client = LLMClient(
        api_key=config.llm_api_key, base_url=config.llm_base_url, model=config.llm_model
    )
    logger.info(f"LLM client initialized: {config.llm_model}")

    # Initialize ChatHandler
    chat_handler = ChatHandler(
        llm_client=llm_client,
        session_maker=database.async_session_maker,
        system_prompt=config.system_prompt,
        max_context_messages=config.max_context_messages,
    )
    logger.info("ChatHandler initialized")

    # Create FastAPI app
    app = create_app(stat_collector, chat_handler)

    # Log startup
    logger.info(f"Starting API server on {config.api_host}:{config.api_port}")
    logger.info(f"StatCollector mode: {config.stat_collector_mode}")
    logger.info("API documentation available at: http://localhost:8000/docs")

    # Run server
    uvicorn.run(
        app,
        host=config.api_host,
        port=config.api_port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
