# GUIDE-06: Codebase Tour

**Цель**: Пройтись по всем файлам проекта с объяснением назначения.

---

## Структура проекта

```
systech-aidd-live/
├── src/                    # Исходный код бота и API
│   ├── main.py            # Точка входа бота
│   ├── api_server.py      # Точка входа API
│   ├── api/               # API модули (FastAPI)
│   ├── models.py          # SQLAlchemy ORM модели
│   ├── database.py        # DB connection management
│   ├── repository.py      # Repository pattern для БД
│   └── ...                # Остальные модули бота
├── frontend/              # Frontend приложение (Next.js)
│   ├── src/               # Исходный код frontend
│   ├── public/            # Статические файлы
│   └── package.json       # Зависимости frontend
├── alembic/               # Миграции базы данных
├── tests/                 # Тесты (unit + integration)
├── prompts/               # Системные промпты
├── doc/                   # Документация
├── logs/                  # Логи (создается автоматически)
├── .venv/                 # Виртуальное окружение (создается uv)
├── docker-compose.yml     # Docker конфигурация для PostgreSQL
├── alembic.ini            # Конфигурация Alembic
├── pyproject.toml         # Зависимости и настройки инструментов
├── uv.lock                # Lock-файл зависимостей
├── Makefile               # Команды автоматизации
├── .env                   # Конфигурация (не в git)
├── .env.example           # Пример конфигурации
└── README.md              # Документация
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

### `models.py` — SQLAlchemy ORM модели

**Файл**: `src/models.py` (~70 строк)

**Назначение**: Определяет структуру таблиц PostgreSQL через ORM.

**Модели**:

1. **`User`** (строки 14-30):
   - `id` (PK) — Telegram user_id (BigInteger)
   - `created_at` — дата создания с timezone
   - `is_deleted` — soft delete флаг
   - `messages` — relationship к Message

2. **`Message`** (строки 33-57):
   - `id` (PK) — автоинкремент
   - `user_id` (FK) — ссылка на users
   - `chat_id` — Telegram chat_id (BigInteger)
   - `role` — роль сообщения (String(20))
   - `content` — текст сообщения (Text)
   - `content_length` — длина сообщения (Integer)
   - `created_at` — дата создания с timezone
   - `is_deleted` — soft delete флаг
   - `user` — relationship к User

**Индексы** (строки 60-68):
- `idx_messages_user_chat` — составной индекс для быстрого поиска сообщений
- `idx_users_active` — индекс для фильтрации активных пользователей

---

### `database.py` — Управление подключением к БД

**Файл**: `src/database.py` (~55 строк)

**Назначение**: Lifecycle управление async сессиями PostgreSQL.

**Ключевые функции**:

1. **`init_database`** (строки 15-22):
   - Создает async engine
   - Создает async_sessionmaker
   - Настраивает connection pool

2. **`close_database`** (строки 25-33):
   - Закрывает все соединения при остановке бота
   - Вызывается в finally блоке main.py

3. **`get_session`** (строки 35-52):
   - Async context manager для получения сессии
   - Автоматический rollback при ошибках
   - Используется в Repository

**Глобальные переменные**:
- `engine` — SQLAlchemy async engine
- `async_session_maker` — фабрика для создания сессий

---

### `repository.py` — Repository pattern

**Файл**: `src/repository.py` (~150 строк)

**Назначение**: Инкапсуляция логики работы с БД.

**Ключевые методы**:

1. **`ensure_user`** (строки 20-43):
   - Проверяет существование пользователя
   - Создает нового пользователя если не существует
   - Возвращает User модель

2. **`add_message`** (строки 45-75):
   - Создает новое сообщение в БД
   - Автоматически вызывает ensure_user
   - Возвращает Message модель

3. **`get_messages`** (строки 77-124):
   - Получает последние N сообщений для контекста
   - System prompt всегда первый (не учитывается в лимите)
   - Возвращает список Message моделей

4. **`soft_delete_messages`** (строки 126-150):
   - Помечает сообщения как удаленные (is_deleted=True)
   - Не удаляет физически из БД
   - Возвращает количество удаленных сообщений

---

### `api_server.py` — Точка входа API

**Файл**: `src/api_server.py` (~90 строк)

**Назначение**: Запуск FastAPI сервера.

**Ключевые операции** (функция `main`):
1. Загрузка конфигурации из .env
2. Инициализация database
3. Выбор StatCollector (mock/real)
4. Создание LLMClient для chat API
5. Создание ChatHandler
6. Создание FastAPI app через create_app
7. Запуск uvicorn сервера

**Endpoints**:
- `/api/v1/statistics` — статистика сообщений
- `/api/v1/chat/message` — отправка сообщения
- `/api/v1/chat/history` — история чата
- `/docs` — Swagger UI
- `/health` — health check

---

### `message.py` — Data class для LLM

**Файл**: `src/message.py` (13 строк)

**Назначение**: Простой data class для передачи в LLM API (отдельно от ORM моделей).

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

## 📁 src/api/ — API модули

### `main.py` — FastAPI приложение

**Файл**: `src/api/main.py`

**Назначение**: Создание FastAPI приложения и регистрация роутов.

**Ключевые функции**:
- `create_app(stat_collector, chat_handler)` — фабрика FastAPI app
- Регистрирует endpoints для statistics и chat
- Настраивает CORS для frontend
- Добавляет health check endpoint

### `schemas.py` — Pydantic схемы для Statistics

**Файл**: `src/api/schemas.py`

**Назначение**: Pydantic модели для валидации и документации API.

**Схемы**:
- `OverviewStats` — общая статистика
- `MessagesByRole` — распределение по ролям
- `TimeSeriesEntry` — точка временного ряда
- `TopMetrics` — ключевые показатели
- `StatisticsResponse` — полный ответ statistics endpoint

### `chat_schemas.py` — Pydantic схемы для Chat

**Файл**: `src/api/chat_schemas.py`

**Назначение**: Pydantic модели для chat API.

**Схемы**:
- `ChatMessageRequest` — запрос на отправку сообщения
- `ChatMessageResponse` — ответ с ответом бота
- `ChatHistoryMessage` — сообщение в истории
- `ChatHistoryResponse` — список истории сообщений

### `protocols.py` — Protocol интерфейсы для API

**Файл**: `src/api/protocols.py`

**Назначение**: Абстракция для StatCollector.

**Protocol**:
- `StatCollectorProtocol` — интерфейс для получения статистики
  - `async def get_statistics(period: str) -> dict`

### `stat_collector_mock.py` — Mock реализация

**Файл**: `src/api/stat_collector_mock.py`

**Назначение**: Генерация тестовых данных для разработки frontend.

**Особенности**:
- Генерирует реалистичные данные
- Поддерживает разные периоды (day/week/month/all)
- Не требует реальной БД

### `stat_collector_real.py` — Real реализация

**Файл**: `src/api/stat_collector_real.py`

**Назначение**: Получение реальной статистики из PostgreSQL.

**Особенности**:
- Использует SQLAlchemy для запросов к БД
- Группировка по времени (час/день/месяц)
- Фильтрация по периоду
- Агрегация статистики

### `chat_handler.py` — Обработчик chat API

**Файл**: `src/api/chat_handler.py`

**Назначение**: Обработка chat сообщений через REST API.

**Режимы**:
- `normal` — обычный чат с LLM
- `admin` — админ режим с text2sql возможностями

**Методы**:
- `handle_message()` — обработка входящего сообщения
- `get_history()` — получение истории чата

---

## 📁 frontend/ — Frontend приложение

**Технологии**: Next.js 15 + TypeScript + shadcn/ui + Tailwind CSS

**Структура**:
```
frontend/
├── src/
│   ├── app/               # Next.js App Router pages
│   │   ├── dashboard/     # Dashboard страница
│   │   └── chat/          # Chat страница
│   ├── components/        # React компоненты
│   │   ├── dashboard/     # Компоненты dashboard
│   │   ├── chat/          # Компоненты chat
│   │   ├── shared/        # Общие компоненты
│   │   └── ui/            # shadcn/ui базовые компоненты
│   └── config/            # Конфигурация
├── public/                # Статические файлы
└── package.json           # Зависимости (управляется pnpm)
```

**Страницы**:
- `/dashboard` — визуализация статистики сообщений и пользователей
- `/chat` — web-интерфейс для чата с ботом

**Команды**:
- `make frontend-install` — установка зависимостей
- `make frontend-dev` — запуск dev сервера
- `make frontend-build` — production build

---

## 📁 alembic/ — Миграции базы данных

**Файлы**:
- `env.py` — конфигурация Alembic для async SQLAlchemy
- `versions/` — директория с миграциями
  - `09eb92e9cbfc_create_users_and_messages_tables.py` — первая миграция

**Команды**:
- `make db-migrate` — применить миграции
- `make db-rollback` — откатить последнюю миграцию
- `make db-revision message="название"` — создать новую миграцию

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

**Backend код**:
- 16 файлов в `src/` (включая api/)
- ~1500 строк кода Python
- PostgreSQL БД с 2 таблицами

**Frontend код**:
- Next.js 15 приложение
- TypeScript + shadcn/ui
- 2 основные страницы (dashboard, chat)

**Тесты**:
- 9 файлов в `tests/`
- Unit + integration тесты
- High code coverage

**Документация**:
- README.md
- 6 гайдов онбординга
- 7 ADR файлов
- API документация (Swagger UI)

**Зависимости**:
- Runtime: aiogram, openai, fastapi, sqlalchemy, asyncpg, alembic, uvicorn
- Dev: pytest, ruff, mypy, pytest-cov, httpx
- Frontend: next, react, typescript, tailwindcss, shadcn/ui

---

## Что дальше?

Переходите к следующим гайдам:
- **GUIDE-07**: Development Workflow — как добавлять новые фичи
- **GUIDE-08**: Testing — как писать и запускать тесты

