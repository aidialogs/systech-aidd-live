import pytest

from src.context_manager import ContextManager
from src.message import Message


@pytest.mark.asyncio
async def test_context_manager_operations(context_manager: ContextManager) -> None:
    """Test basic context manager operations."""
    # Проверка пустого контекста
    context = await context_manager.get_context(123, 456)
    assert context == []

    # Добавление сообщений
    msg1 = Message("user", "Hello")
    msg2 = Message("assistant", "Hi there!")
    msg3 = Message("user", "How are you?")

    await context_manager.add_message(123, 456, msg1)
    await context_manager.add_message(123, 456, msg2)
    await context_manager.add_message(123, 456, msg3)

    # Проверка получения контекста
    context = await context_manager.get_context(123, 456)
    assert len(context) == 3
    assert context[0].content == "Hello"
    assert context[1].content == "Hi there!"
    assert context[2].content == "How are you?"

    # Проверка изоляции контекстов разных пользователей
    msg4 = Message("user", "Different user")
    await context_manager.add_message(789, 789, msg4)

    context1 = await context_manager.get_context(123, 456)
    context2 = await context_manager.get_context(789, 789)

    assert len(context1) == 3
    assert len(context2) == 1
    assert context2[0].content == "Different user"

    # Проверка очистки контекста
    await context_manager.clear_context(123, 456)
    context = await context_manager.get_context(123, 456)
    assert context == []

    # Проверка что другой контекст не затронут
    context2 = await context_manager.get_context(789, 789)
    assert len(context2) == 1


@pytest.mark.asyncio
async def test_context_trimming(context_manager: ContextManager) -> None:
    """Test that context is trimmed when max_context_messages is exceeded."""
    # Use custom context manager with limit 5
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    from src import models

    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    cm = ContextManager(session_maker, max_context_messages=5)

    # Добавить system prompt
    system_msg = Message("system", "You are a helpful assistant")
    await cm.add_message(100, 200, system_msg)

    # Добавить 10 сообщений (превысит лимит 5)
    for i in range(10):
        user_msg = Message("user", f"Message {i}")
        assistant_msg = Message("assistant", f"Response {i}")
        await cm.add_message(100, 200, user_msg)
        await cm.add_message(100, 200, assistant_msg)

    # Проверка что контекст обрезан до 5 сообщений
    context = await cm.get_context(100, 200)
    assert len(context) == 5

    # Проверка что system prompt сохранен
    assert context[0].role == "system"
    assert context[0].content == "You are a helpful assistant"

    # Проверка что сохранены последние сообщения
    assert "Message 9" in context[-2].content or "Response 9" in context[-1].content

    await engine.dispose()


@pytest.mark.asyncio
async def test_clear_nonexistent_context(context_manager: ContextManager) -> None:
    """Test clearing context that doesn't exist."""
    # Clear context that was never created
    await context_manager.clear_context(999, 888)

    # Should not raise error, just log
    context = await context_manager.get_context(999, 888)
    assert context == []
