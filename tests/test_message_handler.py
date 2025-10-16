"""Tests for MessageHandler class."""

from unittest.mock import AsyncMock, Mock

import pytest

from src.command_handler import CommandHandler
from src.context_manager import ContextManager
from src.exceptions import LLMError
from src.message import Message
from src.message_handler import MessageHandler

SetupHandlerTuple = tuple[MessageHandler, AsyncMock, ContextManager, CommandHandler, AsyncMock]


@pytest.fixture
def setup_handler(mock_db_repository: AsyncMock) -> SetupHandlerTuple:
    """Set up MessageHandler with mocked dependencies."""
    mock_llm = AsyncMock()
    mock_llm.get_response = AsyncMock(return_value="AI response")

    context_manager = ContextManager(mock_db_repository, max_context_messages=20)
    command_handler = CommandHandler(context_manager, "Test system prompt")

    handler = MessageHandler(
        llm_client=mock_llm,
        context_manager=context_manager,
        command_handler=command_handler,
        system_prompt="Test system prompt",
    )

    return handler, mock_llm, context_manager, command_handler, mock_db_repository


@pytest.mark.asyncio
async def test_handle_command(setup_handler: SetupHandlerTuple) -> None:
    """Test that commands are handled by CommandHandler."""
    handler, mock_llm, _context_manager, _command_handler, _mock_db_repo = setup_handler

    msg = Mock()
    msg.text = "/start"

    response = await handler.handle_message(msg, 123, 456)

    assert "Привет" in response or "AI-ассистент" in response
    # LLM should not be called for commands
    mock_llm.get_response.assert_not_called()


@pytest.mark.asyncio
async def test_handle_regular_message(setup_handler: SetupHandlerTuple) -> None:
    """Test handling of regular (non-command) messages."""
    handler, mock_llm, context_manager, _, mock_db_repo = setup_handler

    msg = Mock()
    msg.text = "Hello, bot!"

    # Mock empty context initially, then return messages after they're added
    system_msg = Message("system", "Test system prompt")
    user_msg = Message("user", "Hello, bot!")
    assistant_msg = Message("assistant", "AI response")

    # add_message internally calls get_messages for trimming check
    mock_db_repo.get_messages.side_effect = [
        [],  # get_context - empty initially
        [system_msg],  # add_message(system) checks context size
        [system_msg, user_msg],  # add_message(user) checks context size
        [system_msg, user_msg],  # get_context for LLM call
        [system_msg, user_msg, assistant_msg],  # add_message(assistant) checks context size
    ]

    response = await handler.handle_message(msg, 123, 456)

    assert response == "AI response"
    # Verify LLM was called
    mock_llm.get_response.assert_called_once()

    # Verify save_message was called 3 times (system, user, assistant)
    assert mock_db_repo.save_message.call_count == 3


@pytest.mark.asyncio
async def test_handle_none_text(mock_db_repository: AsyncMock) -> None:
    """Test handling message with None text."""
    mock_llm = AsyncMock()
    context_manager = ContextManager(mock_db_repository, 20)
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
    handler, _mock_llm, context_manager, _, mock_db_repo = setup_handler

    msg = Mock()
    msg.text = "First message"

    system_msg = Message("system", "Test system prompt")
    user_msg = Message("user", "First message")
    assistant_msg = Message("assistant", "AI response")

    mock_db_repo.get_messages.side_effect = [
        [],  # get_context - empty initially
        [system_msg],  # add_message(system) checks context size
        [system_msg, user_msg],  # add_message(user) checks context size
        [system_msg, user_msg],  # get_context for LLM call
        [system_msg, user_msg, assistant_msg],  # add_message(assistant) checks context size
    ]

    await handler.handle_message(msg, 999, 888)

    # Verify system prompt was saved
    first_call = mock_db_repo.save_message.call_args_list[0]
    assert first_call[0] == (999, 888, "system", "Test system prompt")


@pytest.mark.asyncio
async def test_llm_error_handling(setup_handler: SetupHandlerTuple) -> None:
    """Test handling of LLM errors."""
    handler, mock_llm, _context_manager, _command_handler, mock_db_repo = setup_handler

    system_msg = Message("system", "Test system prompt")
    user_msg = Message("user", "Test message")

    # Setup mock for empty context and message additions
    mock_db_repo.get_messages.side_effect = [
        [],  # get_context - empty initially
        [system_msg],  # add_message(system) checks context size
        [system_msg, user_msg],  # add_message(user) checks context size
        [system_msg, user_msg],  # get_context for LLM call
    ]

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
    handler, mock_llm, _context_manager, _command_handler, mock_db_repo = setup_handler

    system_msg = Message("system", "Test system prompt")
    user_msg = Message("user", "Test message")

    # Setup mock for empty context and message additions
    mock_db_repo.get_messages.side_effect = [
        [],  # get_context - empty initially
        [system_msg],  # add_message(system) checks context size
        [system_msg, user_msg],  # add_message(user) checks context size
        [system_msg, user_msg],  # get_context for LLM call
    ]

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
    handler, _mock_llm, context_manager, _, mock_db_repo = setup_handler

    msg1 = Mock()
    msg1.text = "First"

    msg2 = Mock()
    msg2.text = "Second"

    system_msg = Message("system", "Test system prompt")
    user_msg1 = Message("user", "First")
    assistant_msg1 = Message("assistant", "AI response")
    user_msg2 = Message("user", "Second")
    assistant_msg2 = Message("assistant", "AI response")

    # First message: get_context, 3x add_message (system, user, assistant), get_context for LLM
    # Second message: get_context, 2x add_message (user, assistant), get_context for LLM
    mock_db_repo.get_messages.side_effect = [
        # First message
        [],  # get_context - empty initially
        [system_msg],  # add_message(system) checks size
        [system_msg, user_msg1],  # add_message(user) checks size
        [system_msg, user_msg1],  # get_context for LLM
        [system_msg, user_msg1, assistant_msg1],  # add_message(assistant) checks size
        # Second message
        [system_msg, user_msg1, assistant_msg1],  # get_context - existing context
        [system_msg, user_msg1, assistant_msg1, user_msg2],  # add_message(user) checks size
        [system_msg, user_msg1, assistant_msg1, user_msg2],  # get_context for LLM
        [system_msg, user_msg1, assistant_msg1, user_msg2, assistant_msg2],  # add_message(assistant) checks size
    ]

    await handler.handle_message(msg1, 111, 222)
    await handler.handle_message(msg2, 111, 222)

    # Verify messages were saved: system + user1 + asst1 + user2 + asst2 = 5
    assert mock_db_repo.save_message.call_count == 5
