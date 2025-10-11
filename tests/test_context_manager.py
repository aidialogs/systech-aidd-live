from src.context_manager import ContextManager
from src.message import Message


def test_context_manager_operations() -> None:
    """Test basic context manager operations."""
    cm = ContextManager(max_context_messages=20)

    # Проверка пустого контекста
    context = cm.get_context(123, 456)
    assert context == []

    # Добавление сообщений
    msg1 = Message("user", "Hello")
    msg2 = Message("assistant", "Hi there!")
    msg3 = Message("user", "How are you?")

    cm.add_message(123, 456, msg1)
    cm.add_message(123, 456, msg2)
    cm.add_message(123, 456, msg3)

    # Проверка получения контекста
    context = cm.get_context(123, 456)
    assert len(context) == 3
    assert context[0].content == "Hello"
    assert context[1].content == "Hi there!"
    assert context[2].content == "How are you?"

    # Проверка изоляции контекстов разных пользователей
    msg4 = Message("user", "Different user")
    cm.add_message(789, 789, msg4)

    context1 = cm.get_context(123, 456)
    context2 = cm.get_context(789, 789)

    assert len(context1) == 3
    assert len(context2) == 1
    assert context2[0].content == "Different user"

    # Проверка очистки контекста
    cm.clear_context(123, 456)
    context = cm.get_context(123, 456)
    assert context == []

    # Проверка что другой контекст не затронут
    context2 = cm.get_context(789, 789)
    assert len(context2) == 1


def test_context_trimming() -> None:
    """Test that context is trimmed when max_context_messages is exceeded."""
    cm = ContextManager(max_context_messages=5)

    # Добавить system prompt
    system_msg = Message("system", "You are a helpful assistant")
    cm.add_message(100, 200, system_msg)

    # Добавить 10 сообщений (превысит лимит 5)
    for i in range(10):
        user_msg = Message("user", f"Message {i}")
        assistant_msg = Message("assistant", f"Response {i}")
        cm.add_message(100, 200, user_msg)
        cm.add_message(100, 200, assistant_msg)

    # Проверка что контекст обрезан до 5 сообщений
    context = cm.get_context(100, 200)
    assert len(context) == 5

    # Проверка что system prompt сохранен
    assert context[0].role == "system"
    assert context[0].content == "You are a helpful assistant"

    # Проверка что сохранены последние сообщения
    assert "Message 9" in context[-2].content or "Response 9" in context[-1].content
