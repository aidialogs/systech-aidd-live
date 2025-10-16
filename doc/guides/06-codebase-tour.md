# GUIDE-06: Codebase Tour

**Цель**: Пройтись по всем файлам проекта с объяснением назначения.

---

## Структура проекта

```
systech-aidd-live/
├── src/                    # Исходный код (10 файлов)
├── tests/                  # Тесты (8 файлов)
├── prompts/                # Системные промпты
├── doc/                    # Документация
├── logs/                   # Логи (создается автоматически)
├── .venv/                  # Виртуальное окружение (создается uv)
├── pyproject.toml          # Зависимости и настройки инструментов
├── uv.lock                 # Lock-файл зависимостей
├── Makefile                # Команды автоматизации
├── .env                    # Конфигурация (не в git)
├── .env.example            # Пример конфигурации
└── README.md               # Документация
```

---

## 📁 src/ — Исходный код

### `main.py` — Точка входа

**Файл**: `src/main.py` (67 строк)

**Назначение**: Запуск бота и инициализация всех компонентов.

**Ключевые операции**:
1. Загрузка `.env` через `load_dotenv()`
2. Создание `Config` из переменных окружения
3. Настройка логирования (файл + консоль)
4. Инициализация компонентов:
   - `Bot` (aiogram)
   - `Dispatcher` (aiogram)
   - `LLMClient`
   - `ContextManager`
   - `CommandHandler`
   - `MessageHandler`
5. Регистрация обработчика сообщений
6. Запуск polling (бесконечный цикл)

**Entry point**: `if __name__ == "__main__": asyncio.run(main())`

---

### `config.py` — Конфигурация

**Файл**: `src/config.py` (77 строк)

**Назначение**: Dataclass для загрузки и валидации настроек из `.env`.

**Ключевые особенности**:
- **`@dataclass`** — структура данных с type hints
- **`Config.from_env()`** — classmethod для загрузки из environment
- **Валидация**: Проверяет наличие обязательных полей, бросает `ConfigError` если отсутствуют
- **System prompt**: Загружает из файла → fallback на env var → default
- **Логирование**: Логирует источник загрузки промпта

**Поля**:
- `bot_token: str` — токен Telegram
- `llm_api_key: str` — ключ LLM API
- `llm_base_url: str` — URL провайдера
- `llm_model: str` — название модели
- `system_prompt: str` — системный промпт
- `max_context_messages: int` — лимит контекста (default: 20)

---

### `message_handler.py` — Координатор

**Файл**: `src/message_handler.py` (74 строки)

**Назначение**: Оркестрирует обработку всех входящих сообщений.

**Ключевая логика** (строки 26-73):
1. Проверка на текстовое сообщение (строка 29)
2. Делегирование команд в `CommandHandler` (строка 35)
3. Если не команда:
   - Получить контекст (строка 42)
   - Добавить system prompt если контекст пустой (строки 45-47)
   - Добавить user message (строки 50-51)
   - Запрос к LLM (строка 60)
   - Добавить assistant message (строки 63-64)
4. Обработка ошибок:
   - `LLMError` → дружелюбное сообщение (строки 68-70)
   - Любая другая → generic сообщение (строки 71-73)

**Зависимости** (через Protocols):
- `LLMClientProtocol`
- `ContextManagerProtocol`
- `CommandHandler`

---

### `command_handler.py` — Обработчик команд

**Файл**: `src/command_handler.py` (45 строк)

**Назначение**: Обрабатывает команды бота (`/start`, `/help`, `/reset`, `/role`).

**Метод `handle_command`** (строки 15-34):
- Принимает текст сообщения
- Возвращает `str` если команда, `None` если не команда
- Логирует выполнение команд

**Команды**:
- `/start` (строки 17-19): Приветствие
- `/help` (строки 21-23): Список команд через `_get_help_text()`
- `/reset` (строки 25-28): Очистка контекста через `context_manager.clear_context()`
- `/role` (строки 30-32): Показ system prompt

**Принцип**: Single Responsibility — только команды, ничего больше.

---

### `context_manager.py` — Управление памятью

**Файл**: `src/context_manager.py` (58 строк)

**Назначение**: Хранит историю диалогов в памяти.

**Структура хранилища** (строка 10):
```python
contexts: dict[tuple[int, int], list[Message]]
```

**Ключевые методы**:

1. **`add_message`** (строки 17-42):
   - Добавляет сообщение в контекст
   - Создает новый контекст если не существует (строки 21-23)
   - **Обрезка контекста** (строки 32-42):
     - Если размер > `max_context_messages`
     - Сохраняет system prompt (первое сообщение)
     - Удаляет старые сообщения
     - Логирует операцию

2. **`get_context`** (строки 44-47):
   - Возвращает список `Message` для `(user_id, chat_id)`
   - Пустой список если контекст не существует

3. **`clear_context`** (строки 49-57):
   - Удаляет контекст для `(user_id, chat_id)`
   - Логирует операцию

---

### `llm_client.py` — Клиент к LLM API

**Файл**: `src/llm_client.py` (46 строк)

**Назначение**: Отправляет запросы к OpenAI-compatible API.

**Метод `get_response`** (строки 17-45):

1. Засекает время выполнения (строка 19)
2. Конвертирует `Message` → dict (строка 22)
3. Логирует запрос: модель, размер контекста (строка 24)
4. Делает async запрос через `AsyncOpenAI` (строки 26-29)
5. Логирует ответ: длительность, статус (строка 32)
6. Проверяет на пустой ответ (строки 35-36)
7. Обработка ошибок (строки 40-45):
   - Все исключения → `LLMError`
   - Логирование с деталями

**Зависимости**:
- `openai.AsyncOpenAI` — async клиент
- `src.exceptions.LLMError` — custom exception

---

### `message.py` — Структура сообщения

**Файл**: `src/message.py` (13 строк)

**Назначение**: Data class для представления сообщения.

**Поля**:
- `role: str` — "system", "user" или "assistant"
- `content: str` — текст сообщения

**Метод `to_dict`** (строки 11-13):
- Конвертирует в формат OpenAI API: `{"role": "...", "content": "..."}`

---

### `protocols.py` — Protocol интерфейсы

**Файл**: `src/protocols.py` (30 строк)

**Назначение**: Определяет контракты для Dependency Injection.

**Protocols**:
1. **`LLMClientProtocol`** (строки 8-13):
   - Абстракция для LLM клиента
   - Метод: `async def get_response(messages) -> str`

2. **`ContextManagerProtocol`** (строки 16-29):
   - Абстракция для менеджера контекста
   - Методы: `add_message`, `get_context`, `clear_context`

**Зачем?**
- Легко мокать в тестах
- Dependency Inversion Principle
- Можно заменить реализацию без изменения кода

---

### `exceptions.py` — Custom исключения

**Файл**: `src/exceptions.py` (9 строк)

**Назначение**: Явные типы ошибок для разных сценариев.

**Exceptions**:
1. **`ConfigError`** (строки 4-6):
   - Ошибки конфигурации (отсутствующие env vars)
   - Приводит к падению при старте

2. **`LLMError`** (строки 8-9):
   - Ошибки LLM API (timeout, unauthorized, etc.)
   - Перехватывается в `MessageHandler` → дружелюбное сообщение

---

## 📁 tests/ — Тесты

### `conftest.py` — Общие фикстуры

**Файл**: `tests/conftest.py` (63 строки)

**Назначение**: Переиспользуемые компоненты для тестов.

**Fixtures**:
1. **`clean_env`** (строки 12-24, autouse=True):
   - Очищает env vars перед каждым тестом
   - Обеспечивает изоляцию тестов

2. **`context_manager`** (строки 27-30):
   - Реальный `ContextManager` для тестов
   - Лимит 20 сообщений

3. **`mock_llm_client`** (строки 33-38):
   - Mock для LLM клиента
   - Возвращает "Mocked LLM response"

4. **`command_handler`** (строки 41-44):
   - Реальный `CommandHandler`

5. **`sample_message`** (строки 47-50):
   - Пример `Message` для тестов

6. **`mock_telegram_message`** (строки 53-62):
   - Mock Telegram сообщения
   - user_id=12345, chat_id=67890

---

### Тестовые файлы

#### `test_message.py` — 4 теста
- Создание Message
- Конвертация в dict
- Разные роли (system, user, assistant)

#### `test_config.py` — 5 тестов
- Загрузка из env
- Валидация обязательных полей
- Загрузка system prompt из файла
- Fallback на env var
- ConfigError при отсутствии полей

#### `test_command_handler.py` — 6 тестов
- Команды: /start, /help, /reset, /role
- Не-команды возвращают None
- Очистка контекста при /reset

#### `test_message_handler.py` — 7 тестов
- Обработка обычных сообщений
- Обработка команд
- Создание контекста при первом сообщении
- Обработка ошибок LLM
- Не-текстовые сообщения

#### `test_llm_client.py` — 4 теста
- 3 unit теста с моками
- 1 integration тест (реальный API вызов)
- Обработка ошибок API

#### `test_context_manager.py` — 3 теста
- Добавление и получение сообщений
- Обрезка контекста при превышении лимита
- Очистка контекста

#### `test_integration.py` — 1 тест
- Интеграционный тест обрезки контекста
- Реальный LLM вызов
- Помечен `@pytest.mark.integration`

---

## 📁 prompts/ — Системные промпты

### `system_prompt.txt`

```
Ты AICodingExpert - профессиональный ИИ-ассистент...
```

**Назначение**: Определяет роль и стиль общения бота.

**Содержание**:
- Экспертиза (код, ревью, debugging, архитектура)
- Стиль общения (профессиональный, с примерами, объяснение "почему")

**Загрузка**: В `Config.from_env()` (строки 53-64 в `config.py`)

---

## 📁 doc/ — Документация

```
doc/
├── guides/              # Гайды (этот файл здесь)
├── adrs/                # Architecture Decision Records (5 файлов)
├── vision.md            # Техническое видение
├── tasklist.md          # План разработки
├── tasklist_tech_debt.md # План устранения техдолга
└── reviews/             # Code review отчеты
```

---

## 📄 Корневые файлы

### `pyproject.toml`

**Секции**:
1. **`[project]`** (строки 1-10):
   - Metadata проекта
   - Зависимости: aiogram, openai, python-dotenv

2. **`[project.optional-dependencies]`** (строки 12-20):
   - dev зависимости: pytest, ruff, mypy, pytest-cov, pytest-mock

3. **`[tool.ruff]`** (строки 29-35):
   - Настройки линтера: line-length=100, правила проверки

4. **`[tool.mypy]`** (строки 37-41):
   - Настройки type checker: strict mode

5. **`[tool.pytest.ini_options]`** (строки 43-49):
   - Настройки pytest: asyncio_mode, coverage, маркеры

6. **`[tool.coverage.run]`** (строки 51-53):
   - Исключения из coverage: tests/, main.py

---

### `Makefile`

**Команды**:
- **Development**: `install`, `run`
- **Testing**: `test`, `test-cov`, `test-integration`, `test-all`
- **Code Quality**: `format`, `lint`, `check-all`
- **Utilities**: `clean`

**Особенность**: Все команды запускаются через `uv run` для правильного окружения.

---

### `.env.example`

Пример конфигурации для копирования в `.env`.

**Обязательные**:
```bash
BOT_TOKEN=your_telegram_bot_token
LLM_API_KEY=your_openrouter_api_key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet
```

**Опциональные**:
```bash
SYSTEM_PROMPT_FILE=prompts/system_prompt.txt
MAX_CONTEXT_MESSAGES=20
```

---

### `uv.lock`

**Назначение**: Фиксирует точные версии зависимостей.

**Зачем?**
- Воспроизводимость окружения
- Все разработчики используют одинаковые версии
- Защита от breaking changes в зависимостях

**Не редактируется вручную** — управляется `uv`.

---

## Навигация по коду

### Где искать что:

**Точка входа**:
→ `src/main.py` (строка 15-66: функция `main()`)

**Обработка сообщения**:
→ `src/message_handler.py` (строка 26-73: метод `handle_message`)

**Команды бота**:
→ `src/command_handler.py` (строка 15-34: метод `handle_command`)

**Управление контекстом**:
→ `src/context_manager.py` (строки 17-42: метод `add_message` с обрезкой)

**Запрос к LLM**:
→ `src/llm_client.py` (строки 17-45: метод `get_response`)

**Конфигурация**:
→ `src/config.py` (строки 20-76: метод `from_env`)

**Тестирование**:
→ `tests/conftest.py` (фикстуры)
→ `tests/test_*.py` (тесты для каждого модуля)

---

## Метрики проекта

**Код**:
- 10 файлов в `src/`
- ~500 строк кода (без комментариев и пустых строк)

**Тесты**:
- 8 файлов в `tests/`
- 30 тестов
- 100% code coverage

**Документация**:
- README.md (365 строк)
- vision.md (661 строка)
- 5 ADR файлов
- 5 гайдов (включая этот)

**Зависимости**:
- 3 runtime: aiogram, openai, python-dotenv
- 5 dev: pytest, ruff, mypy, pytest-cov, pytest-mock

---

## Что дальше?

Переходите к следующим гайдам:
- **GUIDE-07**: Development Workflow — как добавлять новые фичи
- **GUIDE-08**: Testing — как писать и запускать тесты

