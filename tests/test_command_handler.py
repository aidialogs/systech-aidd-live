"""Tests for CommandHandler class."""

from src.command_handler import CommandHandler
from src.context_manager import ContextManager


def test_command_start() -> None:
    """Test /start command."""
    cm = ContextManager(max_context_messages=20)
    handler = CommandHandler(cm)

    response = handler.handle_command("/start", 123, 456)

    assert response is not None
    assert "Привет" in response or "AI-ассистент" in response


def test_command_help() -> None:
    """Test /help command."""
    cm = ContextManager(max_context_messages=20)
    handler = CommandHandler(cm)

    response = handler.handle_command("/help", 123, 456)

    assert response is not None
    assert "/start" in response
    assert "/help" in response
    assert "/reset" in response


def test_command_reset() -> None:
    """Test /reset command."""
    cm = ContextManager(max_context_messages=20)
    handler = CommandHandler(cm)

    # Add some messages first
    from src.message import Message

    cm.add_message(123, 456, Message("user", "Hello"))
    assert len(cm.get_context(123, 456)) == 1

    # Reset
    response = handler.handle_command("/reset", 123, 456)

    assert response is not None
    assert "очищена" in response.lower() or "cleared" in response.lower()
    assert len(cm.get_context(123, 456)) == 0


def test_non_command_returns_none() -> None:
    """Test that non-command text returns None."""
    cm = ContextManager(max_context_messages=20)
    handler = CommandHandler(cm)

    response = handler.handle_command("Hello, how are you?", 123, 456)

    assert response is None


def test_invalid_command_returns_none() -> None:
    """Test that invalid command returns None."""
    cm = ContextManager(max_context_messages=20)
    handler = CommandHandler(cm)

    response = handler.handle_command("/unknown", 123, 456)

    assert response is None


def test_get_help_text() -> None:
    """Test _get_help_text private method."""
    cm = ContextManager(max_context_messages=20)
    handler = CommandHandler(cm)

    help_text = handler._get_help_text()

    assert "Доступные команды" in help_text
    assert "/start" in help_text
    assert "/help" in help_text
    assert "/reset" in help_text
    assert "/role" in help_text


def test_command_role() -> None:
    """Test /role command returns system prompt."""
    cm = ContextManager(max_context_messages=20)
    system_prompt = "I am a test AI assistant"
    handler = CommandHandler(cm, system_prompt)

    response = handler.handle_command("/role", 123, 456)

    assert response is not None
    assert system_prompt in response


def test_help_includes_role_command() -> None:
    """Test /help command includes /role in the list."""
    cm = ContextManager(max_context_messages=20)
    handler = CommandHandler(cm, "Test prompt")

    response = handler.handle_command("/help", 123, 456)

    assert response is not None
    assert "/role" in response
