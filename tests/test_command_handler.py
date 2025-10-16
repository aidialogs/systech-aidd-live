"""Tests for CommandHandler class."""

import pytest

from src.command_handler import CommandHandler
from src.context_manager import ContextManager


@pytest.mark.asyncio
async def test_command_start(command_handler: CommandHandler) -> None:
    """Test /start command."""
    response = await command_handler.handle_command("/start", 123, 456)

    assert response is not None
    assert "Привет" in response or "AI-ассистент" in response


@pytest.mark.asyncio
async def test_command_help(command_handler: CommandHandler) -> None:
    """Test /help command."""
    response = await command_handler.handle_command("/help", 123, 456)

    assert response is not None
    assert "/start" in response
    assert "/help" in response
    assert "/reset" in response


@pytest.mark.asyncio
async def test_command_reset(
    context_manager: ContextManager, command_handler: CommandHandler
) -> None:
    """Test /reset command."""
    # Add some messages first
    from src.message import Message

    await context_manager.add_message(123, 456, Message("user", "Hello"))
    context = await context_manager.get_context(123, 456)
    assert len(context) == 1

    # Reset
    response = await command_handler.handle_command("/reset", 123, 456)

    assert response is not None
    assert "очищена" in response.lower() or "cleared" in response.lower()
    context = await context_manager.get_context(123, 456)
    assert len(context) == 0


@pytest.mark.asyncio
async def test_non_command_returns_none(command_handler: CommandHandler) -> None:
    """Test that non-command text returns None."""
    response = await command_handler.handle_command("Hello, how are you?", 123, 456)

    assert response is None


@pytest.mark.asyncio
async def test_invalid_command_returns_none(command_handler: CommandHandler) -> None:
    """Test that invalid command returns None."""
    response = await command_handler.handle_command("/unknown", 123, 456)

    assert response is None


@pytest.mark.asyncio
async def test_get_help_text(command_handler: CommandHandler) -> None:
    """Test _get_help_text private method."""
    help_text = command_handler._get_help_text()

    assert "Доступные команды" in help_text
    assert "/start" in help_text
    assert "/help" in help_text
    assert "/reset" in help_text
    assert "/role" in help_text


@pytest.mark.asyncio
async def test_command_role(context_manager: ContextManager) -> None:
    """Test /role command returns system prompt."""
    system_prompt = "I am a test AI assistant"
    handler = CommandHandler(context_manager, system_prompt)

    response = await handler.handle_command("/role", 123, 456)

    assert response is not None
    assert system_prompt in response


@pytest.mark.asyncio
async def test_help_includes_role_command(context_manager: ContextManager) -> None:
    """Test /help command includes /role in the list."""
    handler = CommandHandler(context_manager, "Test prompt")

    response = await handler.handle_command("/help", 123, 456)

    assert response is not None
    assert "/role" in response
