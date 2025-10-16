"""Shared fixtures for tests."""

from unittest.mock import AsyncMock, Mock

import pytest

from src.command_handler import CommandHandler
from src.context_manager import ContextManager
from src.database import DatabaseRepository
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
        "DATABASE_URL",
    ]
    for var in env_vars_to_remove:
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def mock_db_repository() -> AsyncMock:
    """Create a mock DatabaseRepository."""
    repo = AsyncMock(spec=DatabaseRepository)
    repo.save_message = AsyncMock()
    repo.get_messages = AsyncMock(return_value=[])
    repo.delete_messages = AsyncMock()
    return repo


@pytest.fixture
def context_manager(mock_db_repository: AsyncMock) -> ContextManager:
    """Create a ContextManager instance with mocked database."""
    return ContextManager(mock_db_repository, max_context_messages=20)


@pytest.fixture
def mock_llm_client() -> AsyncMock:
    """Create a mock LLM client."""
    client = AsyncMock()
    client.get_response = AsyncMock(return_value="Mocked LLM response")
    return client


@pytest.fixture
def command_handler(mock_db_repository: AsyncMock) -> CommandHandler:
    """Create a CommandHandler instance with mocked database."""
    context_manager = ContextManager(mock_db_repository, max_context_messages=20)
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
