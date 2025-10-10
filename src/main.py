import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

from src.config import Config
from src.message_handler import MessageHandler
from src.llm_client import LLMClient


async def main():
    load_dotenv()
    
    config = Config()
    
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )
    
    logging.info("Bot started")
    
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    
    llm_client = LLMClient(
        api_key=config.llm_api_key,
        base_url=config.llm_base_url,
        model=config.llm_model
    )
    
    message_handler = MessageHandler(llm_client, config.system_prompt)
    
    @dp.message()
    async def handle(message: types.Message):
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


if __name__ == '__main__':
    asyncio.run(main())


