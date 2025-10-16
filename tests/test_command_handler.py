"""Tests for CommandHandler class."""

from unittest.mock import AsyncMock

import pytest

from src.command_handler import CommandHandler
from src.context_manager import ContextManager
from src.message import Message


@pytest.mark.asyncio
async def test_command_start(mock_db_repository: AsyncMock) -> None:
    """Test /start command."""
    cm = ContextManager(mock_db_repository, max_context_messages=20)
    handler = CommandHandler(cm)

    response = await handler.handle_command("/start", 123, 456)

    assert response is not None
    assert "Привет" in response or "AI-ассистент" in response


@pytest.mark.asyncio
async def test_command_help(mock_db_repository: AsyncMock) -> None:
    """Test /help command."""
    cm = ContextManager(mock_db_repository, max_context_messages=20)
    handler = CommandHandler(cm)

    response = await handler.handle_command("/help", 123, 456)

    assert response is not None
    assert "/start" in response
    assert "/help" in response
    assert "/reset" in response


@pytest.mark.asyncio
async def test_command_reset(mock_db_repository: AsyncMock) -> None:
    """Test /reset command."""
    cm = ContextManager(mock_db_repository, max_context_messages=20)
    handler = CommandHandler(cm)

    # Setup mock to return a message before reset
    mock_db_repository.get_messages.return_value = [Message("user", "Hello")]

    # Reset
    response = await handler.handle_command("/reset", 123, 456)

    assert response is not None
    assert "очищена" in response.lower() or "cleared" in response.lower()
    mock_db_repository.delete_messages.assert_called_with(123, 456)


@pytest.mark.asyncio
async def test_non_command_returns_none(mock_db_repository: AsyncMock) -> None:
    """Test that non-command text returns None."""
    cm = ContextManager(mock_db_repository, max_context_messages=20)
    handler = CommandHandler(cm)

    response = await handler.handle_command("Hello, how are you?", 123, 456)

    assert response is None


@pytest.mark.asyncio
async def test_invalid_command_returns_none(mock_db_repository: AsyncMock) -> None:
    """Test that invalid command returns None."""
    cm = ContextManager(mock_db_repository, max_context_messages=20)
    handler = CommandHandler(cm)

    response = await handler.handle_command("/unknown", 123, 456)

    assert response is None


def test_get_help_text(mock_db_repository: AsyncMock) -> None:
    """Test _get_help_text private method."""
    cm = ContextManager(mock_db_repository, max_context_messages=20)
    handler = CommandHandler(cm)

    help_text = handler._get_help_text()

    assert "Доступные команды" in help_text
    assert "/start" in help_text
    assert "/help" in help_text
    assert "/reset" in help_text
    assert "/role" in help_text


@pytest.mark.asyncio
async def test_command_role(mock_db_repository: AsyncMock) -> None:
    """Test /role command returns system prompt."""
    cm = ContextManager(mock_db_repository, max_context_messages=20)
    system_prompt = "I am a test AI assistant"
    handler = CommandHandler(cm, system_prompt)

    response = await handler.handle_command("/role", 123, 456)

    assert response is not None
    assert system_prompt in response


@pytest.mark.asyncio
async def test_help_includes_role_command(mock_db_repository: AsyncMock) -> None:
    """Test /help command includes /role in the list."""
    cm = ContextManager(mock_db_repository, max_context_messages=20)
    handler = CommandHandler(cm, "Test prompt")

    response = await handler.handle_command("/help", 123, 456)

    assert response is not None
    assert "/role" in response
