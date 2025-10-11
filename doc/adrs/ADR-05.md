# ADR-05: Архитектурный рефакторинг (SOLID, DRY, Protocols)

**Статус:** Принято  
**Дата:** 2025-10-11  
**Контекст:** Устранение технического долга, Итерация 2

---

## Контекст

После добавления type hints выявлены архитектурные проблемы:
- `MessageHandler` имеет слишком много ответственностей
- Команды смешаны с обработкой обычных сообщений
- Дублирование кода (`(user_id, chat_id)` tuple в 5 местах)
- Прямые зависимости затрудняют тестирование
- Нарушение SRP (Single Responsibility Principle)

## Решение

### 1. Выделить CommandHandler (SRP)

**Проблема:** `MessageHandler` обрабатывает и команды, и обычные сообщения.

**Решение:**
```python
class CommandHandler:
    """Handles bot commands like /start, /help, /reset."""
    
    def __init__(self, context_manager: ContextManagerProtocol) -> None:
        self.context_manager = context_manager

    def handle_command(self, text: str, user_id: int, chat_id: int) -> str | None:
        """Handle command and return response, or None if not a command."""
        if text == "/start":
            return "Привет! Я AI-ассистент..."
        if text == "/help":
            return self._get_help_text()
        if text == "/reset":
            self.context_manager.clear_context(user_id, chat_id)
            return "История диалога очищена..."
        return None  # Not a command
```

**Преимущества:**
- ✅ Один класс = одна ответственность
- ✅ Легко добавлять новые команды
- ✅ Легко тестировать отдельно

### 2. Protocols для Dependency Injection (DIP)

**Проблема:** Прямые зависимости от конкретных классов затрудняют тестирование.

**Решение:**
```python
# protocols.py
class LLMClientProtocol(Protocol):
    """Protocol for LLM client implementations."""
    async def get_response(self, messages: list[Message]) -> str: ...

class ContextManagerProtocol(Protocol):
    """Protocol for context manager implementations."""
    def add_message(self, user_id: int, chat_id: int, message: Message) -> None: ...
    def get_context(self, user_id: int, chat_id: int) -> list[Message]: ...
    def clear_context(self, user_id: int, chat_id: int) -> None: ...

# message_handler.py
class MessageHandler:
    def __init__(
        self,
        llm_client: LLMClientProtocol,  # Используем Protocol, не конкретный класс
        context_manager: ContextManagerProtocol,
        command_handler: CommandHandler,
        system_prompt: str,
    ) -> None: ...
```

**Преимущества:**
- ✅ Легко заменить реализацию (для тестов или production)
- ✅ Зависимость от абстракции, не от конкретики (DIP)
- ✅ Упрощает моки в тестах

### 3. Устранение дублирования (DRY)

**Проблема:** Tuple `(user_id, chat_id)` создается в 5 местах в `ContextManager`.

**Решение:**
```python
class ContextManager:
    def _get_key(self, user_id: int, chat_id: int) -> tuple[int, int]:
        """Get storage key for user and chat."""
        return (user_id, chat_id)

    def add_message(self, user_id: int, chat_id: int, message: Message) -> None:
        key = self._get_key(user_id, chat_id)  # Используем метод
        ...

    def get_context(self, user_id: int, chat_id: int) -> list[Message]:
        key = self._get_key(user_id, chat_id)  # Используем метод
        ...
```

**Преимущества:**
- ✅ Один источник истины для генерации ключа
- ✅ Легко изменить логику (например, добавить хэширование)
- ✅ DRY principle соблюден

## Альтернативы

**Вариант 1: Оставить все в MessageHandler**
- ❌ Нарушение SRP
- ❌ Сложно тестировать
- ❌ Большой класс

**Вариант 2: ABC вместо Protocols**
- ❌ Более строгие требования (нужно наследование)
- ❌ Сложнее в использовании
- ✅ Protocols более гибкие (structural subtyping)

**Вариант 3: Фабрики для DI**
- ❌ Оверинжиниринг для простого проекта
- ✅ Protocols достаточно

## Последствия

**Положительные:**
- ✅ Улучшена тестируемость (легко мокировать через Protocols)
- ✅ SRP соблюден (CommandHandler отделен)
- ✅ DRY соблюден (_get_key метод)
- ✅ Dependency Inversion Principle (зависимости через абстракции)
- ✅ Код более читаемый и поддерживаемый

**Отрицательные:**
- ⚠️ Больше файлов (protocols.py, command_handler.py)
- ⚠️ Нужно обновить main.py для инициализации CommandHandler

**Метрики:**
- Новых файлов: +2 (`protocols.py`, `command_handler.py`)
- Ruff warnings: 0 → 0 (без регрессий)
- Mypy errors: 0 → 0 (без регрессий)
- Test coverage: 42% → 78% (на следующей итерации 100%)

## Архитектура после рефакторинга

```
MessageHandler
    ├── LLMClientProtocol (llm_client)
    ├── ContextManagerProtocol (context_manager)
    ├── CommandHandler (command_handler)
    └── system_prompt: str

CommandHandler
    └── ContextManagerProtocol (context_manager)
```

**Поток обработки:**
1. Message → MessageHandler
2. MessageHandler → CommandHandler.handle_command()
3. Если команда → возврат ответа
4. Если не команда → MessageHandler обрабатывает как сообщение
5. MessageHandler → ContextManager (контекст)
6. MessageHandler → LLMClient (ответ)
7. Ответ → Message

## Примеры использования

**Раньше (все в MessageHandler):**
```python
# 60+ строк в одном методе handle_message
if text == "/start":
    return "..."
if text == "/help":
    return "..."
# ... mixed command handling and message processing
```

**Теперь (разделены ответственности):**
```python
# MessageHandler.handle_message
command_response = self.command_handler.handle_command(text, user_id, chat_id)
if command_response:
    return command_response

# Обработка обычного сообщения
...
```

## Ссылки

- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Python Protocols (PEP 544)](https://peps.python.org/pep-0544/)
- [Dependency Inversion Principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)
- [DRY Principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)

