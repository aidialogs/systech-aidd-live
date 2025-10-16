"""Tests for database repository."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.database import DatabaseRepository
from src.message import Message


@pytest.fixture
def mock_pool() -> MagicMock:
    """Create a mock connection pool."""
    from unittest.mock import MagicMock
    
    pool = MagicMock()
    mock_conn = MagicMock()
    mock_cursor = AsyncMock()

    # Create async context manager for connection
    pool.connection.return_value = AsyncMock()
    pool.connection.return_value.__aenter__.return_value = mock_conn
    pool.connection.return_value.__aexit__.return_value = None

    # Create async context manager for cursor - cursor() is sync, returns async context manager
    cursor_ctx = AsyncMock()
    cursor_ctx.__aenter__.return_value = mock_cursor
    cursor_ctx.__aexit__.return_value = None
    mock_conn.cursor.return_value = cursor_ctx

    # Setup cursor methods
    mock_cursor.execute = AsyncMock()
    mock_cursor.fetchall = AsyncMock(return_value=[])
    mock_cursor.rowcount = 0

    # Setup connection methods - commit() needs to be async
    mock_conn.commit = AsyncMock()

    return pool


@pytest.mark.asyncio
async def test_save_message(mock_pool: MagicMock) -> None:
    """Test saving a message to database."""
    repo = DatabaseRepository(mock_pool)

    await repo.save_message(123, 456, "user", "Hello, world!")

    # Verify connection was acquired
    mock_pool.connection.assert_called_once()

    # Get mock objects to verify calls
    mock_conn = mock_pool.connection.return_value.__aenter__.return_value
    mock_cursor = mock_conn.cursor.return_value.__aenter__.return_value

    # Verify SQL was executed
    mock_cursor.execute.assert_called_once()
    args = mock_cursor.execute.call_args[0]
    assert "INSERT INTO messages" in args[0]
    assert args[1] == (123, 456, "user", "Hello, world!")


@pytest.mark.asyncio
async def test_get_messages(mock_pool: MagicMock) -> None:
    """Test retrieving messages from database."""
    repo = DatabaseRepository(mock_pool)

    # Setup mock data - psycopg with dict_row returns dicts
    mock_conn = mock_pool.connection.return_value.__aenter__.return_value
    mock_cursor = mock_conn.cursor.return_value.__aenter__.return_value
    mock_cursor.fetchall = AsyncMock(return_value=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ])

    messages = await repo.get_messages(123, 456, 20)

    # Verify SQL was executed
    mock_cursor.execute.assert_called_once()
    args = mock_cursor.execute.call_args[0]
    assert "SELECT role, content" in args[0]
    assert "FROM messages" in args[0]
    assert "WHERE user_id = %s AND chat_id = %s" in args[0]
    assert "ORDER BY created_at ASC" in args[0]
    assert "LIMIT %s" in args[0]
    assert args[1] == (123, 456, 20)

    # Verify messages were returned
    assert len(messages) == 3
    assert isinstance(messages[0], Message)
    assert messages[0].role == "system"
    assert messages[0].content == "You are a helpful assistant"
    assert messages[1].role == "user"
    assert messages[2].role == "assistant"


@pytest.mark.asyncio
async def test_get_messages_empty(mock_pool: MagicMock) -> None:
    """Test retrieving messages when none exist."""
    repo = DatabaseRepository(mock_pool)

    messages = await repo.get_messages(999, 888, 20)

    assert len(messages) == 0


@pytest.mark.asyncio
async def test_delete_messages(mock_pool: MagicMock) -> None:
    """Test deleting messages from database."""
    repo = DatabaseRepository(mock_pool)

    await repo.delete_messages(123, 456)

    # Get mock objects to verify calls
    mock_conn = mock_pool.connection.return_value.__aenter__.return_value
    mock_cursor = mock_conn.cursor.return_value.__aenter__.return_value

    # Verify SQL was executed
    mock_cursor.execute.assert_called_once()
    args = mock_cursor.execute.call_args[0]
    assert "DELETE FROM messages" in args[0]
    assert "WHERE user_id = %s AND chat_id = %s" in args[0]
    assert args[1] == (123, 456)


@pytest.mark.asyncio
async def test_create_connection_pool() -> None:
    """Test creating a connection pool."""
    with patch("src.database.AsyncConnectionPool") as mock_pool_class:
        mock_pool_instance = AsyncMock()
        mock_pool_class.return_value = mock_pool_instance

        from src.database import create_connection_pool

        pool = await create_connection_pool("postgresql://user:pass@localhost/db")

        # Verify pool was created with correct parameters (including open=False)
        mock_pool_class.assert_called_once_with(
            conninfo="postgresql://user:pass@localhost/db",
            min_size=2,
            max_size=10,
            timeout=30.0,
            open=False,
        )

        # Verify pool.open() was called
        mock_pool_instance.open.assert_called_once()

        assert pool == mock_pool_instance

