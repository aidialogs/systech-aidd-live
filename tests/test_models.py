"""Tests for SQLAlchemy ORM models."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src import models


@pytest.mark.asyncio
async def test_user_model_creation(async_session: AsyncSession) -> None:
    """Test creating a User model instance."""
    user = models.User(id=123456)
    async_session.add(user)
    await async_session.commit()

    assert user.id == 123456
    assert user.created_at is not None
    assert user.is_deleted is False


@pytest.mark.asyncio
async def test_message_model_creation(async_session: AsyncSession) -> None:
    """Test creating a Message model instance."""
    # Create user first
    user = models.User(id=123456)
    async_session.add(user)
    await async_session.commit()

    # Create message
    message = models.Message(
        user_id=123456,
        chat_id=789012,
        role="user",
        content="Hello, world!",
        content_length=13,
    )
    async_session.add(message)
    await async_session.commit()

    assert message.id is not None
    assert message.user_id == 123456
    assert message.chat_id == 789012
    assert message.role == "user"
    assert message.content == "Hello, world!"
    assert message.content_length == 13
    assert message.created_at is not None
    assert message.is_deleted is False


@pytest.mark.asyncio
async def test_user_message_relationship(async_session: AsyncSession) -> None:
    """Test relationship between User and Message models."""
    # Create user
    user = models.User(id=123456)
    async_session.add(user)
    await async_session.commit()

    # Create messages
    msg1 = models.Message(
        user_id=123456,
        chat_id=789012,
        role="user",
        content="Message 1",
        content_length=9,
    )
    msg2 = models.Message(
        user_id=123456,
        chat_id=789012,
        role="assistant",
        content="Message 2",
        content_length=9,
    )
    async_session.add_all([msg1, msg2])
    await async_session.commit()

    # Refresh user to load relationships
    await async_session.refresh(user, ["messages"])

    assert len(user.messages) == 2
    assert msg1 in user.messages
    assert msg2 in user.messages


@pytest.mark.asyncio
async def test_message_soft_delete(async_session: AsyncSession) -> None:
    """Test soft delete functionality."""
    # Create user and message
    user = models.User(id=123456)
    async_session.add(user)
    await async_session.commit()

    message = models.Message(
        user_id=123456,
        chat_id=789012,
        role="user",
        content="Test message",
        content_length=12,
    )
    async_session.add(message)
    await async_session.commit()

    # Soft delete
    message.is_deleted = True
    await async_session.commit()

    # Verify soft delete
    assert message.is_deleted is True
    # Message still exists in database
    await async_session.refresh(message)
    assert message.id is not None


@pytest.mark.asyncio
async def test_user_soft_delete(async_session: AsyncSession) -> None:
    """Test soft delete for user."""
    user = models.User(id=123456)
    async_session.add(user)
    await async_session.commit()

    # Soft delete
    user.is_deleted = True
    await async_session.commit()

    # Verify soft delete
    assert user.is_deleted is True
    await async_session.refresh(user)
    assert user.id == 123456
