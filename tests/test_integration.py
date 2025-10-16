"""Integration tests with real PostgreSQL database.

These tests require a running PostgreSQL instance.
Run with: pytest tests/test_integration.py -v
"""

import os

import pytest

from src.context_manager import ContextManager
from src.database import DatabaseRepository, create_connection_pool
from src.message import Message


@pytest.fixture(scope="module")
async def db_pool():
    """Create a real database connection pool for integration tests."""
    # Use DATABASE_URL from environment or default to local instance
    database_url = os.getenv(
        "DATABASE_URL", "postgresql://bot_user:bot_password@localhost:5432/systech_aidd"
    )

    pool = await create_connection_pool(database_url)
    yield pool
    await pool.close()


@pytest.fixture
async def db_repository(db_pool):
    """Create a DatabaseRepository with real connection pool."""
    repo = DatabaseRepository(db_pool)

    # Clean up messages table before each test
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM messages")
            await conn.commit()

    yield repo

    # Clean up after test
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM messages")
            await conn.commit()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_database_save_and_retrieve(db_repository: DatabaseRepository) -> None:
    """Test saving and retrieving messages from real database."""
    user_id, chat_id = 1001, 2001

    # Save messages
    await db_repository.save_message(user_id, chat_id, "system", "You are helpful")
    await db_repository.save_message(user_id, chat_id, "user", "Hello")
    await db_repository.save_message(user_id, chat_id, "assistant", "Hi there!")

    # Retrieve messages
    messages = await db_repository.get_messages(user_id, chat_id, 10)

    # Verify
    assert len(messages) == 3
    assert messages[0].role == "system"
    assert messages[0].content == "You are helpful"
    assert messages[1].role == "user"
    assert messages[1].content == "Hello"
    assert messages[2].role == "assistant"
    assert messages[2].content == "Hi there!"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_database_delete_messages(db_repository: DatabaseRepository) -> None:
    """Test deleting messages from real database."""
    user_id, chat_id = 1002, 2002

    # Save messages
    await db_repository.save_message(user_id, chat_id, "user", "Test message 1")
    await db_repository.save_message(user_id, chat_id, "assistant", "Test response 1")

    # Verify they exist
    messages = await db_repository.get_messages(user_id, chat_id, 10)
    assert len(messages) == 2

    # Delete messages
    await db_repository.delete_messages(user_id, chat_id)

    # Verify they're gone
    messages = await db_repository.get_messages(user_id, chat_id, 10)
    assert len(messages) == 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_database_message_isolation(db_repository: DatabaseRepository) -> None:
    """Test that messages for different users/chats are isolated."""
    # User 1 in Chat 1
    await db_repository.save_message(1, 1, "user", "User1 Chat1")
    # User 2 in Chat 2
    await db_repository.save_message(2, 2, "user", "User2 Chat2")
    # User 1 in Chat 2
    await db_repository.save_message(1, 2, "user", "User1 Chat2")

    # Check isolation
    messages_1_1 = await db_repository.get_messages(1, 1, 10)
    messages_2_2 = await db_repository.get_messages(2, 2, 10)
    messages_1_2 = await db_repository.get_messages(1, 2, 10)

    assert len(messages_1_1) == 1
    assert messages_1_1[0].content == "User1 Chat1"

    assert len(messages_2_2) == 1
    assert messages_2_2[0].content == "User2 Chat2"

    assert len(messages_1_2) == 1
    assert messages_1_2[0].content == "User1 Chat2"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_context_manager_with_real_database(db_repository: DatabaseRepository) -> None:
    """Test ContextManager with real database backend."""
    cm = ContextManager(db_repository, max_context_messages=20)
    user_id, chat_id = 1003, 2003

    # Add system prompt
    system_msg = Message("system", "You are a helpful assistant")
    await cm.add_message(user_id, chat_id, system_msg)

    # Add user and assistant messages
    user_msg = Message("user", "What is Python?")
    await cm.add_message(user_id, chat_id, user_msg)

    assistant_msg = Message("assistant", "Python is a programming language.")
    await cm.add_message(user_id, chat_id, assistant_msg)

    # Get context
    context = await cm.get_context(user_id, chat_id)

    # Verify
    assert len(context) == 3
    assert context[0].role == "system"
    assert context[1].role == "user"
    assert context[2].role == "assistant"

    # Clear context
    await cm.clear_context(user_id, chat_id)

    # Verify cleared
    context = await cm.get_context(user_id, chat_id)
    assert len(context) == 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_context_trimming_with_real_database(db_repository: DatabaseRepository) -> None:
    """Test context trimming with real database - system prompt preservation."""
    cm = ContextManager(db_repository, max_context_messages=20)
    user_id, chat_id = 1004, 2004

    # Add system prompt
    system_msg = Message("system", "You are a helpful AI assistant")
    await cm.add_message(user_id, chat_id, system_msg)

    # Add many messages to trigger trimming (30 pairs = 60 messages + 1 system = 61 total)
    for i in range(30):
        user_msg = Message("user", f"Question {i}")
        assistant_msg = Message("assistant", f"Answer {i}")
        await cm.add_message(user_id, chat_id, user_msg)
        await cm.add_message(user_id, chat_id, assistant_msg)

    # Get context
    context = await cm.get_context(user_id, chat_id)

    # Verify trimming
    assert len(context) == 20, f"Expected 20 messages, got {len(context)}"

    # Verify system prompt is preserved
    assert context[0].role == "system"
    assert context[0].content == "You are a helpful AI assistant"

    # Verify old messages are removed
    contents = [m.content for m in context]
    assert "Question 0" not in contents
    assert "Question 1" not in contents
    assert "Answer 0" not in contents

    # Verify recent messages are kept
    assert "Question 29" in contents or "Answer 29" in contents

    print(f"✅ Context trimming works correctly:")
    print(f"   Total messages: {len(context)}")
    print(f"   First: {context[0].role} - {context[0].content[:40]}...")
    print(f"   Last: {context[-1].role} - {context[-1].content[:40]}...")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_concurrent_users_with_real_database(db_repository: DatabaseRepository) -> None:
    """Test that multiple users can use the system concurrently."""
    cm = ContextManager(db_repository, max_context_messages=20)

    # Simulate 3 concurrent users
    users_data = [
        (2001, 3001, "User A"),
        (2002, 3002, "User B"),
        (2003, 3003, "User C"),
    ]

    # Each user adds messages
    for user_id, chat_id, name in users_data:
        await cm.add_message(user_id, chat_id, Message("system", f"System for {name}"))
        await cm.add_message(user_id, chat_id, Message("user", f"Hello from {name}"))
        await cm.add_message(
            user_id, chat_id, Message("assistant", f"Hi {name}, how can I help?")
        )

    # Verify each user has their own context
    for user_id, chat_id, name in users_data:
        context = await cm.get_context(user_id, chat_id)
        assert len(context) == 3
        assert f"{name}" in context[0].content or f"{name}" in context[1].content


@pytest.mark.integration
@pytest.mark.asyncio
async def test_database_ordering(db_repository: DatabaseRepository) -> None:
    """Test that messages are returned in correct chronological order."""
    user_id, chat_id = 1005, 2005

    # Add messages with slight delays to ensure ordering
    messages_to_add = [
        ("system", "System prompt"),
        ("user", "First question"),
        ("assistant", "First answer"),
        ("user", "Second question"),
        ("assistant", "Second answer"),
    ]

    for role, content in messages_to_add:
        await db_repository.save_message(user_id, chat_id, role, content)

    # Retrieve messages
    messages = await db_repository.get_messages(user_id, chat_id, 10)

    # Verify order
    assert len(messages) == 5
    for i, (expected_role, expected_content) in enumerate(messages_to_add):
        assert messages[i].role == expected_role
        assert messages[i].content == expected_content


@pytest.mark.integration
@pytest.mark.asyncio
async def test_database_limit(db_repository: DatabaseRepository) -> None:
    """Test that get_messages respects the limit parameter."""
    user_id, chat_id = 1006, 2006

    # Add 10 messages
    for i in range(10):
        await db_repository.save_message(user_id, chat_id, "user", f"Message {i}")

    # Request only 5
    messages = await db_repository.get_messages(user_id, chat_id, 5)

    # Verify we got only 5 (the most recent ones)
    assert len(messages) == 5
    # Should be messages 5-9 (0-indexed, but we want the last 5)
    assert messages[0].content == "Message 5"
    assert messages[-1].content == "Message 9"
