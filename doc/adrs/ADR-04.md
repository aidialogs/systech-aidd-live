# ADR-04: Type Hints и валидация конфигурации

**Статус:** Принято  
**Дата:** 2025-10-11  
**Контекст:** Устранение технического долга, Итерация 1

---

## Контекст

После внедрения mypy обнаружено 64 ошибки типов:
- Отсутствие type hints во всех функциях и методах
- `Config` - обычный класс без валидации
- Нет проверки обязательных env переменных
- Ошибки конфигурации выявляются поздно (в runtime)
- Нет явных типов для исключений

## Решение

**1. Добавить type hints везде (100% покрытие):**
```python
def handle_message(self, message: types.Message, user_id: int, chat_id: int) -> str:
    """Handle incoming message and return bot response."""
    ...
```

**2. Превратить Config в dataclass с валидацией:**
```python
@dataclass
class Config:
    """Application configuration loaded from environment variables."""
    
    bot_token: str
    llm_api_key: str
    llm_base_url: str
    llm_model: str
    system_prompt: str
    max_context_messages: int

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables with validation."""
        # Валидация обязательных полей
        missing = []
        if not (bot_token := os.getenv("BOT_TOKEN")):
            missing.append("BOT_TOKEN")
        # ...
        
        if missing:
            raise ConfigError(f"Missing required environment variables: {', '.join(missing)}")
        
        return cls(bot_token=bot_token, ...)
```

**3. Создать custom exceptions:**
```python
class ConfigError(Exception):
    """Exception raised for configuration errors."""

class LLMError(Exception):
    """Exception raised for LLM API errors."""
```

**4. Использовать type narrowing для обработки None:**
```python
# После валидации используем assert для type narrowing
assert bot_token is not None
```

## Альтернативы

**Вариант 1: Pydantic для Config**
- ❌ Дополнительная зависимость
- ❌ Overkill для простой конфигурации
- ✅ Dataclass достаточно для наших нужд

**Вариант 2: Оставить без type hints**
- ❌ Нет статической проверки
- ❌ Ошибки обнаруживаются в runtime
- ❌ IDE не подсказывает типы

**Вариант 3: Частичные type hints**
- ❌ Половинчатое решение
- ❌ Mypy все равно будет ругаться
- ✅ Выбрали 100% покрытие

## Последствия

**Положительные:**
- ✅ Mypy errors: 64 → 0
- ✅ Ранняя валидация конфигурации
- ✅ Четкие типы для всех функций
- ✅ IDE autocomplete и type checking
- ✅ Самодокументируемый код
- ✅ Явная обработка ошибок через custom exceptions

**Отрицательные:**
- ⚠️ Больше кода (добавлены type hints)
- ⚠️ Необходимость указывать типы при рефакторинге

**Метрики:**
- Type hints coverage: 0% → 100%
- Mypy errors: 64 → 0 (strict mode)
- Config validation: нет → полная проверка при старте
- Custom exceptions: 0 → 2 (`ConfigError`, `LLMError`)

## Изменения в коде

**Созданные файлы:**
- `src/exceptions.py` - `ConfigError`, `LLMError`

**Обновленные файлы:**
- `src/config.py` - dataclass + `from_env()` + валидация
- `src/message.py` - type hints для `__init__`, `to_dict`
- `src/context_manager.py` - type hints для всех методов
- `src/llm_client.py` - type hints + `LLMError` handling
- `src/message_handler.py` - type hints + error handling
- `src/main.py` - `Config.from_env()`, type hints

**Тесты:**
- Добавлены тесты для `Config.from_env()` с валидацией
- Тесты для missing environment variables

## Примеры использования

**Раньше (без type hints):**
```python
def add_message(self, user_id, chat_id, message):
    key = (user_id, chat_id)
    # IDE не знает типы, могут быть ошибки
```

**Теперь (с type hints):**
```python
def add_message(self, user_id: int, chat_id: int, message: Message) -> None:
    key = (user_id, chat_id)
    # IDE подсказывает типы, mypy проверяет корректность
```

## Ссылки

- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Mypy Strict Mode](https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-strict)

