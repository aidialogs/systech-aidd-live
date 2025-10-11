import logging

from aiogram import types

from src.command_handler import CommandHandler
from src.exceptions import LLMError
from src.message import Message
from src.protocols import ContextManagerProtocol, LLMClientProtocol


class MessageHandler:
    """Handles incoming messages and coordinates bot responses."""

    def __init__(
        self,
        llm_client: LLMClientProtocol,
        context_manager: ContextManagerProtocol,
        command_handler: CommandHandler,
        system_prompt: str,
    ) -> None:
        self.llm_client = llm_client
        self.context_manager = context_manager
        self.command_handler = command_handler
        self.system_prompt = system_prompt

    async def handle_message(self, message: types.Message, user_id: int, chat_id: int) -> str:
        """Handle incoming message and return bot response."""
        text = message.text
        if text is None:
            return "Извините, я могу обрабатывать только текстовые сообщения."

        logging.info(f'Message from user_id={user_id} chat_id={chat_id}: "{text}"')

        # Сначала проверяем команды
        command_response = self.command_handler.handle_command(text, user_id, chat_id)
        if command_response:
            return command_response

        # Если не команда - обрабатываем как обычное сообщение
        try:
            # Получить контекст
            context = self.context_manager.get_context(user_id, chat_id)

            # Добавить system prompt если контекст пустой
            if not context:
                system_message = Message("system", self.system_prompt)
                self.context_manager.add_message(user_id, chat_id, system_message)

            # Добавить user message в контекст
            user_message = Message("user", text)
            self.context_manager.add_message(user_id, chat_id, user_message)

            # Получить обновленный контекст для отправки в LLM
            context = self.context_manager.get_context(user_id, chat_id)

            # Логировать размер контекста
            logging.info(f"Sending to LLM: context_size={len(context)}")

            # Получить ответ от LLM
            response = await self.llm_client.get_response(context)

            # Добавить assistant message в контекст
            assistant_message = Message("assistant", response)
            self.context_manager.add_message(user_id, chat_id, assistant_message)

            return response

        except LLMError as e:
            logging.error(f"LLM error: {e!s}")
            return "Извините, не могу ответить прямо сейчас. Попробуйте чуть позже."
        except Exception as e:
            logging.error(f"Unexpected error handling message: {e!s}")
            return "Извините, произошла ошибка. Попробуйте еще раз."
