from src.context_manager import ContextManager
from src.message import Message


def test_context_manager_operations():
    cm = ContextManager()
    
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



