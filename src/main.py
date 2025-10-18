import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from src import database
from src.command_handler import CommandHandler
from src.config import Config
from src.context_manager import ContextManager
from src.llm_client import LLMClient
from src.message_handler import MessageHandler


async def main() -> None:
    """Main entry point for the bot application."""
    load_dotenv()

    # Configure logging BEFORE loading config (Config.from_env uses logging)
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
    )

    logging.info("Bot started")

    # Load configuration (after logging is configured)
    config = Config.from_env()

    # Initialize database
    database.init_database(config.database_url, config.database_echo)
    logging.info("Database initialized")

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    llm_client = LLMClient(
        api_key=config.llm_api_key, base_url=config.llm_base_url, model=config.llm_model
    )

    # Initialize context manager with session maker
    context_manager = ContextManager(database.async_session_maker, config.max_context_messages)

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
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info("Bot stopped")
    finally:
        await bot.session.close()
        await database.close_database()
        logging.info("Database connections closed")


if __name__ == "__main__":
    asyncio.run(main())
