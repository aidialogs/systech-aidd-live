"""Shared fixtures for tests."""

from unittest.mock import AsyncMock, Mock

import pytest

from src.command_handler import CommandHandler
from src.context_manager import ContextManager
from src.message import Message


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Clean environment variables before each test to ensure isolation."""
    env_vars_to_remove = [
        "BOT_TOKEN",
        "LLM_API_KEY",
        "LLM_BASE_URL",
        "LLM_MODEL",
        "SYSTEM_PROMPT",
        "MAX_CONTEXT_MESSAGES",
    ]
    for var in env_vars_to_remove:
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def context_manager() -> ContextManager:
    """Create a real ContextManager instance for testing."""
    return ContextManager(max_context_messages=20)


@pytest.fixture
def mock_llm_client() -> AsyncMock:
    """Create a mock LLM client."""
    client = AsyncMock()
    client.get_response = AsyncMock(return_value="Mocked LLM response")
    return client


@pytest.fixture
def command_handler(context_manager: ContextManager) -> CommandHandler:
    """Create a CommandHandler instance."""
    return CommandHandler(context_manager)


@pytest.fixture
def sample_message() -> Message:
    """Create a sample Message instance."""
    return Message("user", "Hello, world!")


@pytest.fixture
def mock_telegram_message() -> Mock:
    """Create a mock Telegram message."""
    msg = Mock()
    msg.text = "Test message"
    msg.from_user = Mock()
    msg.from_user.id = 12345
    msg.chat = Mock()
    msg.chat.id = 67890
    return msg
