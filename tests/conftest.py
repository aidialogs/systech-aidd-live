"""Shared fixtures for tests."""

from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src import models
from src.command_handler import CommandHandler
from src.context_manager import ContextManager
from src.message import Message
from src.repository import MessageRepository


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
        "DATABASE_ECHO",
    ]
    for var in env_vars_to_remove:
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create async engine for testing with SQLite in-memory database."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    yield engine

    # Cleanup
    await engine.dispose()


@pytest.fixture
def async_session_maker(async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create async session maker for testing."""
    return async_sessionmaker(async_engine, expire_on_commit=False)


@pytest.fixture
async def async_session(
    async_session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """Create async session for testing."""
    async with async_session_maker() as session:
        yield session


@pytest.fixture
async def repository(async_session: AsyncSession) -> MessageRepository:
    """Create MessageRepository for testing."""
    return MessageRepository(async_session)


@pytest.fixture
def context_manager(async_session_maker: async_sessionmaker[AsyncSession]) -> ContextManager:
    """Create a ContextManager instance with test database for testing."""
    return ContextManager(async_session_maker, max_context_messages=20)


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
