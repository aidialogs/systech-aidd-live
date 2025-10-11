"""Tests for MessageHandler class."""

from unittest.mock import AsyncMock, Mock

import pytest

from src.command_handler import CommandHandler
from src.context_manager import ContextManager
from src.exceptions import LLMError
from src.message_handler import MessageHandler

SetupHandlerTuple = tuple[MessageHandler, AsyncMock, ContextManager, CommandHandler]


@pytest.fixture
def setup_handler() -> SetupHandlerTuple:
    """Set up MessageHandler with mocked dependencies."""
    mock_llm = AsyncMock()
    mock_llm.get_response = AsyncMock(return_value="AI response")

    context_manager = ContextManager(max_context_messages=20)
    command_handler = CommandHandler(context_manager, "Test system prompt")

    handler = MessageHandler(
        llm_client=mock_llm,
        context_manager=context_manager,
        command_handler=command_handler,
        system_prompt="Test system prompt",
    )

    return handler, mock_llm, context_manager, command_handler


@pytest.mark.asyncio
async def test_handle_command(setup_handler: SetupHandlerTuple) -> None:
    """Test that commands are handled by CommandHandler."""
    handler, mock_llm, _context_manager, _ = setup_handler

    msg = Mock()
    msg.text = "/start"

    response = await handler.handle_message(msg, 123, 456)

    assert "Привет" in response or "AI-ассистент" in response
    # LLM should not be called for commands
    mock_llm.get_response.assert_not_called()


@pytest.mark.asyncio
async def test_handle_regular_message(setup_handler: SetupHandlerTuple) -> None:
    """Test handling of regular (non-command) messages."""
    handler, mock_llm, context_manager, _ = setup_handler

    msg = Mock()
    msg.text = "Hello, bot!"

    response = await handler.handle_message(msg, 123, 456)

    assert response == "AI response"
    # Verify LLM was called
    mock_llm.get_response.assert_called_once()

    # Verify context was updated
    context = context_manager.get_context(123, 456)
    assert len(context) == 3  # system + user + assistant
    assert context[0].role == "system"
    assert context[1].role == "user"
    assert context[1].content == "Hello, bot!"
    assert context[2].role == "assistant"


@pytest.mark.asyncio
async def test_handle_none_text() -> None:
    """Test handling message with None text."""
    mock_llm = AsyncMock()
    context_manager = ContextManager(20)
    command_handler = CommandHandler(context_manager, "Test prompt")

    handler = MessageHandler(mock_llm, context_manager, command_handler, "Test prompt")

    msg = Mock()
    msg.text = None

    response = await handler.handle_message(msg, 123, 456)

    assert "текстовые сообщения" in response.lower()
    mock_llm.get_response.assert_not_called()


@pytest.mark.asyncio
async def test_system_prompt_added_on_first_message(setup_handler: SetupHandlerTuple) -> None:
    """Test that system prompt is added on first message."""
    handler, _mock_llm, context_manager, _ = setup_handler

    msg = Mock()
    msg.text = "First message"

    await handler.handle_message(msg, 999, 888)

    context = context_manager.get_context(999, 888)
    assert len(context) == 3
    assert context[0].role == "system"
    assert context[0].content == "Test system prompt"


@pytest.mark.asyncio
async def test_llm_error_handling(setup_handler: SetupHandlerTuple) -> None:
    """Test handling of LLM errors."""
    handler, mock_llm, _context_manager, _ = setup_handler

    # Make LLM raise LLMError
    mock_llm.get_response = AsyncMock(side_effect=LLMError("API error"))

    msg = Mock()
    msg.text = "Test message"

    response = await handler.handle_message(msg, 123, 456)

    assert "Извините" in response
    assert "не могу ответить" in response.lower()


@pytest.mark.asyncio
async def test_unexpected_error_handling(setup_handler: SetupHandlerTuple) -> None:
    """Test handling of unexpected errors."""
    handler, mock_llm, _context_manager, _ = setup_handler

    # Make LLM raise unexpected exception
    mock_llm.get_response = AsyncMock(side_effect=RuntimeError("Unexpected"))

    msg = Mock()
    msg.text = "Test message"

    response = await handler.handle_message(msg, 123, 456)

    assert "Извините" in response
    assert "ошибка" in response.lower()


@pytest.mark.asyncio
async def test_context_persistence_across_messages(setup_handler: SetupHandlerTuple) -> None:
    """Test that context persists across multiple messages."""
    handler, _mock_llm, context_manager, _ = setup_handler

    msg1 = Mock()
    msg1.text = "First"

    msg2 = Mock()
    msg2.text = "Second"

    await handler.handle_message(msg1, 111, 222)
    await handler.handle_message(msg2, 111, 222)

    context = context_manager.get_context(111, 222)
    # system + (user + assistant) * 2 = 5
    assert len(context) == 5
    assert context[0].role == "system"
    assert context[1].content == "First"
    assert context[3].content == "Second"
