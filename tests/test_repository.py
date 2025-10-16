"""Tests for MessageRepository."""

import pytest

from src.repository import MessageRepository


@pytest.mark.asyncio
async def test_ensure_user_creates_new_user(repository: MessageRepository) -> None:
    """Test that ensure_user creates a new user if not exists."""
    user = await repository.ensure_user(123456)
    await repository.session.commit()

    assert user.id == 123456
    assert user.is_deleted is False


@pytest.mark.asyncio
async def test_ensure_user_returns_existing_user(repository: MessageRepository) -> None:
    """Test that ensure_user returns existing user."""
    # Create user first
    user1 = await repository.ensure_user(123456)
    await repository.session.commit()

    # Try to ensure same user
    user2 = await repository.ensure_user(123456)
    await repository.session.commit()

    assert user1.id == user2.id


@pytest.mark.asyncio
async def test_add_message(repository: MessageRepository) -> None:
    """Test adding a message."""
    message = await repository.add_message(
        user_id=123456, chat_id=789012, role="user", content="Hello, world!"
    )
    await repository.session.commit()

    assert message.id is not None
    assert message.user_id == 123456
    assert message.chat_id == 789012
    assert message.role == "user"
    assert message.content == "Hello, world!"
    assert message.content_length == 13
    assert message.is_deleted is False


@pytest.mark.asyncio
async def test_get_messages_empty(repository: MessageRepository) -> None:
    """Test getting messages when none exist."""
    messages = await repository.get_messages(user_id=123456, chat_id=789012, limit=20)

    assert messages == []


@pytest.mark.asyncio
async def test_get_messages_with_system_prompt(repository: MessageRepository) -> None:
    """Test getting messages with system prompt included first."""
    # Add system prompt
    await repository.add_message(
        user_id=123456, chat_id=789012, role="system", content="You are a helpful assistant"
    )
    # Add user messages
    await repository.add_message(user_id=123456, chat_id=789012, role="user", content="Message 1")
    await repository.add_message(
        user_id=123456, chat_id=789012, role="assistant", content="Response 1"
    )
    await repository.session.commit()

    messages = await repository.get_messages(user_id=123456, chat_id=789012, limit=20)

    assert len(messages) == 3
    assert messages[0].role == "system"
    assert messages[0].content == "You are a helpful assistant"
    assert messages[1].content == "Message 1"
    assert messages[2].content == "Response 1"


@pytest.mark.asyncio
async def test_get_messages_respects_limit(repository: MessageRepository) -> None:
    """Test that get_messages respects limit parameter."""
    # Add system prompt
    await repository.add_message(user_id=123456, chat_id=789012, role="system", content="System")
    # Add many messages
    for i in range(10):
        await repository.add_message(
            user_id=123456, chat_id=789012, role="user", content=f"Message {i}"
        )
    await repository.session.commit()

    # Get only last 5
    messages = await repository.get_messages(user_id=123456, chat_id=789012, limit=5)

    assert len(messages) == 5
    assert messages[0].role == "system"  # System prompt always included
    # Should get last 4 messages
    assert "Message 6" in messages[-4].content or "Message 7" in messages[-3].content


@pytest.mark.asyncio
async def test_get_messages_ignores_deleted(repository: MessageRepository) -> None:
    """Test that get_messages ignores deleted messages."""
    # Add messages
    await repository.add_message(user_id=123456, chat_id=789012, role="user", content="Message 1")
    msg2 = await repository.add_message(
        user_id=123456, chat_id=789012, role="user", content="Message 2"
    )
    await repository.session.commit()

    # Soft delete one message
    msg2.is_deleted = True
    await repository.session.commit()

    messages = await repository.get_messages(user_id=123456, chat_id=789012, limit=20)

    assert len(messages) == 1
    assert messages[0].content == "Message 1"


@pytest.mark.asyncio
async def test_get_messages_isolates_chats(repository: MessageRepository) -> None:
    """Test that messages are isolated by chat_id."""
    # Add messages to different chats
    await repository.add_message(user_id=123456, chat_id=111, role="user", content="Chat 1 Message")
    await repository.add_message(user_id=123456, chat_id=222, role="user", content="Chat 2 Message")
    await repository.session.commit()

    messages_chat1 = await repository.get_messages(user_id=123456, chat_id=111, limit=20)
    messages_chat2 = await repository.get_messages(user_id=123456, chat_id=222, limit=20)

    assert len(messages_chat1) == 1
    assert len(messages_chat2) == 1
    assert messages_chat1[0].content == "Chat 1 Message"
    assert messages_chat2[0].content == "Chat 2 Message"


@pytest.mark.asyncio
async def test_soft_delete_messages(repository: MessageRepository) -> None:
    """Test soft deleting messages."""
    # Add messages
    await repository.add_message(user_id=123456, chat_id=789012, role="user", content="Message 1")
    await repository.add_message(user_id=123456, chat_id=789012, role="user", content="Message 2")
    await repository.session.commit()

    # Soft delete
    count = await repository.soft_delete_messages(user_id=123456, chat_id=789012)
    await repository.session.commit()

    assert count == 2

    # Verify messages are marked as deleted
    messages = await repository.get_messages(user_id=123456, chat_id=789012, limit=20)
    assert len(messages) == 0


@pytest.mark.asyncio
async def test_soft_delete_messages_isolates_chats(repository: MessageRepository) -> None:
    """Test that soft delete only affects specific chat."""
    # Add messages to different chats
    await repository.add_message(user_id=123456, chat_id=111, role="user", content="Chat 1")
    await repository.add_message(user_id=123456, chat_id=222, role="user", content="Chat 2")
    await repository.session.commit()

    # Soft delete only chat 1
    count = await repository.soft_delete_messages(user_id=123456, chat_id=111)
    await repository.session.commit()

    assert count == 1

    messages_chat1 = await repository.get_messages(user_id=123456, chat_id=111, limit=20)
    messages_chat2 = await repository.get_messages(user_id=123456, chat_id=222, limit=20)

    assert len(messages_chat1) == 0
    assert len(messages_chat2) == 1


@pytest.mark.asyncio
async def test_soft_delete_messages_returns_zero_when_empty(
    repository: MessageRepository,
) -> None:
    """Test that soft delete returns 0 when no messages to delete."""
    count = await repository.soft_delete_messages(user_id=999999, chat_id=888888)
    await repository.session.commit()

    assert count == 0
