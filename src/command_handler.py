"""Handler for bot commands."""

import logging

from src.protocols import ContextManagerProtocol


class CommandHandler:
    """Handles bot commands like /start, /help, /reset."""

    def __init__(self, context_manager: ContextManagerProtocol) -> None:
        self.context_manager = context_manager

    def handle_command(self, text: str, user_id: int, chat_id: int) -> str | None:
        """Handle command and return response, or None if not a command."""
        if text == "/start":
            logging.info(f"Command /start from user_id={user_id}")
            return "Привет! Я AI-ассистент. Используй /help для справки."

        if text == "/help":
            logging.info(f"Command /help from user_id={user_id}")
            return self._get_help_text()

        if text == "/reset":
            logging.info(f"Command /reset from user_id={user_id}")
            self.context_manager.clear_context(user_id, chat_id)
            return "История диалога очищена. Начнем сначала!"

        return None  # Not a command

    def _get_help_text(self) -> str:
        """Get help text with available commands."""
        return (
            "Доступные команды:\n"
            "/start - Начать диалог\n"
            "/help - Показать эту справку\n"
            "/reset - Очистить историю диалога"
        )
