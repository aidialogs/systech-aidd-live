from src.context_manager import ContextManager
from src.message import Message


def test_context_trimming_with_many_messages() -> None:
    """Тест обрезки контекста при большом количестве сообщений"""
    cm = ContextManager(max_context_messages=20)

    user_id = 999
    chat_id = 888

    # Добавить system prompt
    system_msg = Message("system", "Ты полезный AI-ассистент")
    cm.add_message(user_id, chat_id, system_msg)

    # Добавить 30 пар сообщений (60 сообщений + 1 system = 61 всего)
    for i in range(30):
        user_msg = Message("user", f"Вопрос номер {i}")
        assistant_msg = Message("assistant", f"Ответ номер {i}")
        cm.add_message(user_id, chat_id, user_msg)
        cm.add_message(user_id, chat_id, assistant_msg)

    # Получить контекст
    context = cm.get_context(user_id, chat_id)

    # Проверка что контекст обрезан до 20 сообщений
    assert len(context) == 20, f"Ожидалось 20 сообщений, получено {len(context)}"

    # Проверка что system prompt сохранен
    assert context[0].role == "system"
    assert context[0].content == "Ты полезный AI-ассистент"

    # Проверка что старые сообщения удалены (должны остаться последние)
    assert "Вопрос номер 0" not in str([m.content for m in context])
    assert "Вопрос номер 1" not in str([m.content for m in context])

    # Проверка что последние сообщения сохранены
    assert "Вопрос номер 29" in str([m.content for m in context]) or "Ответ номер 29" in str(
        [m.content for m in context]
    )

    print(f"✅ Контекст успешно обрезан: {len(context)} сообщений")
    print(f"   Первое: {context[0].role} - {context[0].content[:30]}...")
    print(f"   Последнее: {context[-1].role} - {context[-1].content[:30]}...")
