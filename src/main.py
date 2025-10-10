import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

from src.config import Config
from src.message_handler import MessageHandler


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
    message_handler = MessageHandler()
    
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


