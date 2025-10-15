"""Combined entry point for bot and API server."""

import asyncio
import logging
import os

import uvicorn
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from src.api_server import app
from src.command_handler import CommandHandler
from src.config import Config
from src.context_manager import ContextManager
from src.llm_client import LLMClient
from src.message_handler import MessageHandler
from src.mock_stats_collector import MockStatsCollector


async def run_bot(config: Config, context_manager: ContextManager) -> None:
    """Run Telegram bot with polling."""
    logging.info("Starting Telegram bot...")

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    llm_client = LLMClient(
        api_key=config.llm_api_key, base_url=config.llm_base_url, model=config.llm_model
    )

    command_handler = CommandHandler(context_manager, config.system_prompt)

    message_handler = MessageHandler(
        llm_client, context_manager, command_handler, config.system_prompt
    )

    @dp.message()
    async def handle(message: types.Message) -> None:
        """Handle incoming Telegram messages."""
        if message.from_user is None:
            return

        user_id = message.from_user.id
        chat_id = message.chat.id
        response = await message_handler.handle_message(message, user_id, chat_id)
        await message.answer(response)

    try:
        logging.info("Bot started and polling...")
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        logging.info("Bot polling cancelled")
    finally:
        await bot.session.close()
        logging.info("Bot stopped")


async def run_api(config: Config, context_manager: ContextManager) -> None:
    """Run FastAPI server."""
    logging.info("Starting API server...")

    # Create mock stats collector (later can be real one using context_manager)
    stats_collector = MockStatsCollector()

    # Attach to app state
    app.state.stats_collector = stats_collector
    app.state.context_manager = context_manager  # На будущее для реальной статистики

    logging.info(f"API server starting on {config.api_host}:{config.api_port}")

    # Run uvicorn
    config_uvicorn = uvicorn.Config(
        app, host=config.api_host, port=config.api_port, log_level="info"
    )
    server = uvicorn.Server(config_uvicorn)
    await server.serve()


async def main() -> None:
    """Main entry point for combined bot and API server."""
    load_dotenv()
    config = Config.from_env()

    # Setup logging
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
    )

    logging.info("=" * 60)
    logging.info("Starting combined service (Bot + API)")
    logging.info("=" * 60)

    # Shared context manager between bot and API
    context_manager = ContextManager(config.max_context_messages)

    # Run both services concurrently
    try:
        await asyncio.gather(
            run_bot(config, context_manager),
            run_api(config, context_manager),
        )
    except KeyboardInterrupt:
        logging.info("Shutting down services...")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
