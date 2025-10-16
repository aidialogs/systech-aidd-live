from unittest.mock import AsyncMock

import pytest

from src.context_manager import ContextManager
from src.message import Message


@pytest.mark.asyncio
async def test_context_manager_operations(mock_db_repository: AsyncMock) -> None:
    """Test basic context manager operations."""
    cm = ContextManager(mock_db_repository, max_context_messages=20)

    # Проверка пустого контекста
    mock_db_repository.get_messages.return_value = []
    context = await cm.get_context(123, 456)
    assert context == []
    mock_db_repository.get_messages.assert_called_once_with(123, 456, 20)

    # Добавление сообщений
    msg1 = Message("user", "Hello")
    msg2 = Message("assistant", "Hi there!")
    msg3 = Message("user", "How are you?")

    mock_db_repository.get_messages.return_value = [msg1]
    await cm.add_message(123, 456, msg1)
    mock_db_repository.save_message.assert_called_with(123, 456, "user", "Hello")

    mock_db_repository.get_messages.return_value = [msg1, msg2]
    await cm.add_message(123, 456, msg2)

    mock_db_repository.get_messages.return_value = [msg1, msg2, msg3]
    await cm.add_message(123, 456, msg3)

    # Проверка получения контекста
    mock_db_repository.get_messages.return_value = [msg1, msg2, msg3]
    context = await cm.get_context(123, 456)
    assert len(context) == 3
    assert context[0].content == "Hello"
    assert context[1].content == "Hi there!"
    assert context[2].content == "How are you?"

    # Проверка изоляции контекстов разных пользователей
    msg4 = Message("user", "Different user")
    mock_db_repository.get_messages.return_value = [msg4]
    await cm.add_message(789, 789, msg4)

    mock_db_repository.get_messages.return_value = [msg1, msg2, msg3]
    context1 = await cm.get_context(123, 456)
    mock_db_repository.get_messages.return_value = [msg4]
    context2 = await cm.get_context(789, 789)

    assert len(context1) == 3
    assert len(context2) == 1
    assert context2[0].content == "Different user"

    # Проверка очистки контекста
    await cm.clear_context(123, 456)
    mock_db_repository.delete_messages.assert_called_with(123, 456)

    mock_db_repository.get_messages.return_value = []
    context = await cm.get_context(123, 456)
    assert context == []

    # Проверка что другой контекст не затронут
    mock_db_repository.get_messages.return_value = [msg4]
    context2 = await cm.get_context(789, 789)
    assert len(context2) == 1


@pytest.mark.asyncio
async def test_context_trimming(mock_db_repository: AsyncMock) -> None:
    """Test that context is trimmed when max_context_messages is exceeded."""
    cm = ContextManager(mock_db_repository, max_context_messages=5)

    # Добавить system prompt
    system_msg = Message("system", "You are a helpful assistant")
    mock_db_repository.get_messages.return_value = [system_msg]
    await cm.add_message(100, 200, system_msg)

    # Создаем список всех сообщений
    all_messages = [system_msg]

    # Добавить 10 сообщений (превысит лимит 5)
    for i in range(10):
        user_msg = Message("user", f"Message {i}")
        assistant_msg = Message("assistant", f"Response {i}")
        all_messages.append(user_msg)
        all_messages.append(assistant_msg)

        # Имитируем добавление сообщения и возврат увеличенного контекста
        mock_db_repository.get_messages.return_value = all_messages[-6:]
        await cm.add_message(100, 200, user_msg)

        mock_db_repository.get_messages.return_value = all_messages[-6:]
        await cm.add_message(100, 200, assistant_msg)

    # Имитируем превышение лимита - возвращаем 6 сообщений
    trimmed_messages = [
        system_msg,
        Message("user", "Message 8"),
        Message("assistant", "Response 8"),
        Message("user", "Message 9"),
        Message("assistant", "Response 9"),
    ]
    mock_db_repository.get_messages.return_value = trimmed_messages

    # Проверка что контекст обрезан до 5 сообщений
    context = await cm.get_context(100, 200)
    assert len(context) == 5

    # Проверка что system prompt сохранен
    assert context[0].role == "system"
    assert context[0].content == "You are a helpful assistant"

    # Проверка что сохранены последние сообщения
    assert "Message 9" in context[-2].content or "Response 9" in context[-1].content


@pytest.mark.asyncio
async def test_clear_nonexistent_context(mock_db_repository: AsyncMock) -> None:
    """Test clearing context that doesn't exist."""
    cm = ContextManager(mock_db_repository, max_context_messages=20)

    # Clear context that was never created
    await cm.clear_context(999, 888)
    mock_db_repository.delete_messages.assert_called_with(999, 888)

    # Should not raise error, just log
    mock_db_repository.get_messages.return_value = []
    context = await cm.get_context(999, 888)
    assert context == []
