# Техническое видение проекта

## 1. Технологии

### Основной стек
- **Python 3.11+** - базовый язык разработки
- **aiogram 3.x** - асинхронная библиотека для Telegram Bot API
- **openai** - Python SDK для работы с LLM через OpenAI Compatible API
- **python-dotenv** - загрузка переменных окружения из .env файла
- **PostgreSQL 16** - реляционная СУБД для персистентного хранения
- **psycopg[binary] 3.x** - асинхронный драйвер для PostgreSQL
- **yoyo-migrations** - инструмент для управления миграциями БД

### Управление зависимостями и окружением
- **uv** - современный менеджер пакетов и виртуальных окружений
- **pyproject.toml** - описание проекта и зависимостей
- **uv.lock** - фиксация версий зависимостей

### Автоматизация сборки и запуска
- **Makefile** - простые команды для типовых операций:
  - `make install` - установка зависимостей
  - `make run` - запуск бота
  - `make test` - запуск тестов
  - `make lint` - проверка кода

### Тестирование
- **pytest** - минимальный набор unit-тестов для критичных компонентов
- **pytest-asyncio** - поддержка асинхронных тестов
- **pytest-cov** - измерение покрытия тестами
- **pytest-mock** - моки для изоляции тестов
- Покрытие тестами: только ключевая бизнес-логика

### Инструменты качества кода
- **ruff** - современный форматтер и линтер (замена black + flake8 + isort)
- **mypy** - проверка типов (strict mode)
- Запуск через Makefile: `make format`, `make lint`, `make test-cov`
- Без pre-commit hooks - все запускается вручную

### Инфраструктура и деплой
- **Docker Compose** - локальная разработка с PostgreSQL
- **Локальный запуск бота** - `python -m src.main`
- Запуск вручную, без автоматизации CI/CD

---

## 2. Принципы разработки

### Ключевые принципы
- **KISS (Keep It Simple, Stupid)** - никакого оверинжиниринга, только необходимое для проверки идеи
- **Один класс = один файл** - строгое правило для структурированности кода
- **Явное лучше неявного** - простой и понятный код
- **Asyncio** - асинхронный код (т.к. aiogram и openai async)

### Что НЕ используем (для простоты)
- ❌ Сложные паттерны проектирования (фабрики, строители, стратегии)
- ❌ DI-контейнеры и IoC
- ❌ Избыточную абстракцию и многоуровневую иерархию классов
- ❌ Pydantic models (используем простые dataclasses)
- ❌ ORM (SQLAlchemy ORM) - используем прямые SQL запросы
- ❌ Микросервисы
- ❌ Очереди сообщений

### Что используем для качества кода
- ✅ **Type hints** - обязательны для всех функций и методов
- ✅ **Dataclasses** - для структур данных (Config)
- ✅ **Ruff** - форматирование и линтинг
- ✅ **Mypy** - проверка типов (strict mode)
- ✅ **Custom exceptions** - для разных типов ошибок (ConfigError, LLMError)

### Организация кода
- **Классы** - для логических компонентов (MessageHandler, LLMClient, ContextManager) и структур данных (Message)
- **Функции** - для простой обработки данных
- **Config** - простой класс с настройками из переменных окружения

### Стиль кода
- Следуем базовому **PEP 8** (визуально)
- Без автоматических проверок

---

## 3. Структура проекта

### Организация файлов

```
systech-aidd-live/
├── src/
│   ├── __init__.py
│   ├── main.py              # Точка входа, инициализация, запуск polling
│   ├── config.py            # Config dataclass - настройки из .env с валидацией
│   ├── exceptions.py        # Custom exceptions (ConfigError, LLMError)
│   ├── protocols.py         # Protocol interfaces для DI (LLMClientProtocol, ContextManagerProtocol)
│   ├── message.py           # Message класс - структура сообщения
│   ├── command_handler.py   # CommandHandler класс - обработка команд (/start, /help, /reset, /role)
│   ├── message_handler.py   # MessageHandler класс - координация обработки сообщений
│   ├── llm_client.py        # LLMClient класс - работа с LLM API
│   ├── context_manager.py   # ContextManager класс - управление контекстом
│   └── database.py          # DatabaseRepository класс - работа с PostgreSQL
├── migrations/              # Yoyo миграции БД
│   └── 001_initial_schema.sql
├── prompts/
│   └── system_prompt.txt    # Системный промпт для роли AICodingExpert
├── tests/
│   ├── __init__.py
│   ├── test_llm_client.py
│   ├── test_context_manager.py
│   └── test_database.py
├── logs/                    # Директория для логов (создается автоматически)
│   └── app.log
├── docker-compose.yml       # Docker Compose для PostgreSQL
├── yoyo.ini                 # Конфигурация Yoyo migrations
├── .gitignore
├── pyproject.toml           # Зависимости проекта
├── uv.lock                  # Зафиксированные версии
├── Makefile                 # Команды для запуска
└── README.md
```

### Принципы организации
- **Один класс = один файл** - строго соблюдается
- **Плоская структура** - все классы в src/ без вложенных пакетов
- **Минимум файлов** - только необходимое для работы

---

## 4. Архитектура проекта

### Общая схема взаимодействия

```
User (Telegram)
     ↓
[MessageHandler] ← координатор
     ↓          ↓         ↓
[CommandHandler] [ContextManager] [LLMClient]
     ↓              ↓                  ↓
[/start,/help]  [DatabaseRepository] [OpenAI API]
[/reset]           ↓
                [PostgreSQL]
```

### Поток обработки сообщения

1. Пользователь отправляет сообщение в Telegram
2. aiogram Dispatcher передает в MessageHandler.handle_message()
3. MessageHandler:
   - Получает историю диалога от ContextManager.get_context(user_id, chat_id)
   - Добавляет сообщение пользователя через ContextManager.add_message(user_id, chat_id, message)
   - Отправляет полную историю в LLMClient.get_response()
   - Сохраняет ответ LLM через ContextManager.add_message(user_id, chat_id, message)
   - Отправляет ответ пользователю в Telegram
4. При ошибке LLM API - показывает дружелюбное сообщение ("Извините, временные проблемы...")

### Ответственность компонентов

**MessageHandler** (координатор):
- Оркестрирует взаимодействие между CommandHandler, ContextManager и LLMClient
- Делегирует обработку команд в CommandHandler
- Обрабатывает обычные сообщения через LLM
- Обработка ошибок с дружелюбными сообщениями

**CommandHandler** (обработчик команд):
- Отвечает только за обработку команд: /start, /help, /reset, /role
- SRP (Single Responsibility Principle) - одна ответственность
- Зависит только от ContextManager (через Protocol)
- Для команды /role использует Config.system_prompt (содержимое файла промпта)

**ContextManager** (хранилище):
- Управляет историей диалогов через DatabaseRepository
- Ограничение контекста: последние N сообщений (например, 20)
- Очистка контекста по команде
- Асинхронные методы для работы с БД

**DatabaseRepository** (слой данных):
- Работа с PostgreSQL через psycopg3 connection pool
- CRUD операции для messages: save_message, get_messages, delete_messages
- Прямые SQL запросы без ORM

**LLMClient** (клиент внешнего API):
- Отправка запросов к OpenAI Compatible API
- Формирование запросов в формате chat completion
- Возврат текста ответа или exception при ошибке

**Config** (конфигурация):
- Загрузка параметров из .env с валидацией
- Dataclass со строгой типизацией
- Валидация обязательных переменных при старте (Config.from_env())
- Бросает ConfigError если отсутствуют обязательные переменные
- Хранение: bot_token, llm_api_key, llm_base_url, llm_model, system_prompt, max_context_messages, database_url
- System prompt загружается из файла (prompts/system_prompt.txt) или из переменной окружения SYSTEM_PROMPT

### Принципы архитектуры
- **Простота** - минимум слоев и абстракций
- **SRP (Single Responsibility Principle)** - каждый класс имеет одну ответственность
- **DRY (Don't Repeat Yourself)** - нет дублирования кода
- **DIP (Dependency Inversion)** - зависимости через Protocol интерфейсы (для тестируемости)
- **Асинхронность** - async/await для работы с БД и внешними API
- **Персистентность** - PostgreSQL для хранения истории диалогов
- **Stateless LLM** - LLMClient не хранит состояние

### Protocols для Dependency Injection

Используем Protocol interfaces для абстракции зависимостей:
- `LLMClientProtocol` - интерфейс для LLM клиента
- `ContextManagerProtocol` - интерфейс для менеджера контекста

Это позволяет:
- Легко мокать зависимости в тестах
- Соблюдать Dependency Inversion Principle
- Сохранять простоту (без DI-контейнеров)

---

## 5. Модель данных

### Класс Message

Простой класс для структурирования сообщений с type hints:

```python
class Message:
    """Represents a chat message with role and content."""
    
    def __init__(self, role: str, content: str) -> None:
        self.role = role        # "system" | "user" | "assistant"
        self.content = content  # str - текст сообщения
    
    def to_dict(self) -> dict[str, str]:
        """Convert message to dictionary format for API calls."""
        return {"role": self.role, "content": self.content}
```

### Схема базы данных PostgreSQL

Простая таблица `messages` для хранения истории диалогов:

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Индексы для эффективных запросов
CREATE INDEX idx_user_chat ON messages(user_id, chat_id);
CREATE INDEX idx_created_at ON messages(created_at);
```

**Поля:**
- `id` - автоинкрементный первичный ключ
- `user_id` - ID пользователя из Telegram (message.from_user.id)
- `chat_id` - ID чата из Telegram (message.chat.id)
- `role` - роль сообщения ("system", "user", "assistant")
- `content` - текст сообщения
- `created_at` - временная метка создания (для сортировки)

**Индексы:**
- `idx_user_chat` - быстрый поиск по комбинации (user_id, chat_id)
- `idx_created_at` - сортировка сообщений по времени

### DatabaseRepository

Простой репозиторий для работы с БД:

```python
class DatabaseRepository:
    def __init__(self, pool: AsyncConnectionPool) -> None:
        self.pool = pool
    
    async def save_message(user_id: int, chat_id: int, role: str, content: str) -> None:
        """Сохранить сообщение в БД"""
    
    async def get_messages(user_id: int, chat_id: int, limit: int) -> list[Message]:
        """Получить последние N сообщений для пользователя"""
    
    async def delete_messages(user_id: int, chat_id: int) -> None:
        """Удалить все сообщения пользователя (команда /reset)"""
```

### Ограничения и правила

- **max_context_messages**: 20 сообщений (настраивается через Config)
- При превышении лимита - удаляются старые сообщения (кроме system)
- System prompt всегда сохраняется первым
- История сохраняется между перезапусками бота
- Используется connection pool для эффективной работы с БД

### Что используем:
- ✅ **PostgreSQL** - персистентное хранилище
- ✅ **psycopg3** - асинхронный драйвер
- ✅ **Прямые SQL запросы** - без ORM
- ✅ **Yoyo migrations** - версионирование схемы БД

### Что НЕ используем:
- ❌ ORM (SQLAlchemy ORM) - избегаем избыточной абстракции
- ❌ Pydantic models - используем простые dataclasses

---

## 6. Работа с LLM

### Класс LLMClient

Единый класс для работы с OpenAI Compatible API:

```python
class LLMClient:
    def __init__(self, api_key, base_url, model):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    
    async def get_response(self, messages):
        # messages - список объектов Message
        # конвертирует в формат OpenAI: [{"role": "...", "content": "..."}]
        # отправляет запрос к API
        # возвращает текст ответа (str) или raise Exception
```

### Конфигурация провайдера

Через переменные окружения `.env`:

```bash
LLM_API_KEY=sk-or-v1-xxx
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet
SYSTEM_PROMPT=Ты полезный AI-ассистент. Отвечай кратко и по делу.
```

### Провайдер LLM

**Основной провайдер**: OpenRouter
- Доступ к множеству моделей через единый API
- Поддержка OpenAI-совместимого формата
- Удобная оплата и управление

**Альтернативы для разработки/тестирования**:
- Ollama (локально) - для разработки без интернета
- Groq - быстрые ответы для тестирования

### Обработка ошибок

- **Без retry** - при ошибке API сразу возвращаем exception
- MessageHandler перехватывает и показывает пользователю дружелюбное сообщение
- Логируем все ошибки для отладки

### Логирование запросов/ответов

- Логируем каждый запрос к LLM: модель, количество сообщений в контексте
- Логируем каждый ответ: текст ответа, время выполнения
- Логируем ошибки с полным stack trace
- Используется для отладки и анализа работы бота

---

## 7. Мониторинг LLM

### Подход к мониторингу

Минимальный мониторинг через логирование - без внешних систем и метрик.

### Метрики в логах

Каждый запрос к LLM логируется со следующими данными:

- **Timestamp** - время запроса
- **User ID + Chat ID** - идентификация диалога
- **Model** - используемая модель
- **Context size** - количество сообщений в контексте
- **Duration** - время выполнения запроса (секунды)
- **Status** - success/error
- **Error message** - текст ошибки (если есть)

### Пример формата лога

```
2025-10-10 14:23:45 | user_id=12345 chat_id=67890 | model=claude-3.5-sonnet | context_size=5 | duration=1.23s | status=success
2025-10-10 14:24:10 | user_id=12345 chat_id=67890 | model=claude-3.5-sonnet | context_size=7 | duration=0s | status=error | error=Connection timeout
```

### Реализация

- Встроенный модуль `logging` Python
- Файл логов: `logs/app.log`
- Уровни логирования: INFO для успешных запросов, ERROR для ошибок
- Без ротации логов на первом этапе

### Что НЕ используем

- ❌ Prometheus + Grafana
- ❌ БД для метрик (InfluxDB, TimescaleDB)
- ❌ Внешние системы мониторинга (DataDog, New Relic)
- ❌ Алерты и уведомления
- ❌ Подсчет токенов и стоимости
- ❌ Дашборды и визуализация

---

## 8. Сценарии работы

### Основные use cases бота

**1. Первый запуск - команда /start**
- Пользователь отправляет `/start`
- Бот приветствует пользователя
- Бот кратко объясняет свои возможности и доступные команды
- Инициализируется контекст с system prompt

**2. Обычный диалог**
- Пользователь отправляет текстовое сообщение
- Бот получает историю диалога из ContextManager
- Добавляет сообщение пользователя в контекст
- Отправляет полную историю в LLM через LLMClient
- Получает ответ от LLM
- Сохраняет ответ в контекст
- Отправляет ответ пользователю в Telegram

**3. Справка - команда /help**
- Пользователь отправляет `/help`
- Бот показывает список доступных команд и их описание:
  - `/start` - начать работу с ботом
  - `/help` - показать справку
  - `/reset` - очистить историю диалога
  - `/role` - показать информацию о роли ассистента

**4. Сброс контекста - команда /reset**
- Пользователь отправляет `/reset`
- ContextManager очищает историю диалога для (user_id, chat_id)
- Бот подтверждает: "История диалога очищена. Начнем сначала!"

**5. Отображение роли - команда /role**
- Пользователь отправляет `/role`
- Бот показывает информацию о своей роли (содержимое системного промпта)
- Отображается текст из prompts/system_prompt.txt
- Пример: если промпт содержит "Ты AICodingExpert - эксперт по программированию...", то это и показывается пользователю

**6. Обработка ошибок LLM API**
- При ошибке API (timeout, недоступность сервиса, etc.)
- MessageHandler перехватывает exception
- Пользователь видит дружелюбное сообщение:
  - "Извините, не могу ответить прямо сейчас. Попробуйте чуть позже."
- Ошибка логируется для последующего анализа

**7. Длинный диалог (превышение лимита контекста)**
- При превышении max_context_messages (например, 20)
- ContextManager автоматически удаляет старые сообщения
- System prompt всегда сохраняется
- Процесс прозрачен для пользователя - никаких уведомлений
- Диалог продолжается с сокращенным контекстом

### Ограничения MVP
- Только текстовые сообщения (без изображений, файлов, голосовых)
- Один system prompt для всех пользователей
- Без персонализации ответов
- Без истории между перезапусками бота

---

## 9. Подход к конфигурированию

### Метод конфигурации

Все настройки загружаются из переменных окружения через `.env` файл.

### Класс Config

Dataclass для загрузки и валидации настроек:

```python
from dataclasses import dataclass
from src.exceptions import ConfigError

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
        # Бросает ConfigError если переменные отсутствуют
        # Загружает system_prompt из файла prompts/system_prompt.txt
        # или из переменной окружения SYSTEM_PROMPT
        ...
```

### Параметры конфигурации

**Обязательные параметры:**
- `BOT_TOKEN` - токен Telegram бота (получить через @BotFather)
- `LLM_API_KEY` - API ключ для OpenRouter
- `LLM_BASE_URL` - URL провайдера LLM (https://openrouter.ai/api/v1)
- `LLM_MODEL` - название модели (например: anthropic/claude-3.5-sonnet)
- `DATABASE_URL` - строка подключения к PostgreSQL (postgresql://user:password@host:port/database)

**Опциональные параметры (с дефолтами):**
- `SYSTEM_PROMPT` - системный промпт (default: загружается из prompts/system_prompt.txt)
- `SYSTEM_PROMPT_FILE` - путь к файлу с системным промптом (default: "prompts/system_prompt.txt")
- `MAX_CONTEXT_MESSAGES` - лимит сообщений в контексте (default: 20)

### Файлы конфигурации

**.env** (не в git):
```bash
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
LLM_API_KEY=sk-or-v1-xxxxxxxxxxxxx
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet
SYSTEM_PROMPT_FILE=prompts/system_prompt.txt
MAX_CONTEXT_MESSAGES=20
DATABASE_URL=postgresql://bot_user:bot_password@localhost:5432/systech_aidd
```

**.env template:**
```bash
BOT_TOKEN=your_telegram_bot_token
LLM_API_KEY=your_openrouter_api_key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet
SYSTEM_PROMPT_FILE=prompts/system_prompt.txt
MAX_CONTEXT_MESSAGES=20
DATABASE_URL=postgresql://bot_user:bot_password@localhost:5432/systech_aidd
```

### Загрузка .env

Используем библиотеку `python-dotenv`:
```python
from dotenv import load_dotenv
load_dotenv()  # в main.py перед созданием Config
```

### Что НЕ используем

- ❌ YAML/TOML конфигурационные файлы
- ❌ Pydantic Settings (используем простые dataclasses)
- ❌ Конфиг-серверы (Consul, etcd)
- ❌ Множественные окружения (dev/staging/prod)
- ❌ Секреты-менеджеры (Vault, AWS Secrets Manager)

---

## 10. Подход к логгированию

### Метод логгирования

Встроенный модуль `logging` Python - простая настройка без внешних библиотек.

### Уровни логирования

- **INFO** - успешные операции (запуск бота, обработка сообщений, запросы к LLM)
- **ERROR** - ошибки (проблемы с LLM API, исключения)
- **DEBUG** - детальная отладка (опционально, по умолчанию выключено)

### Что логируем

**Lifecycle события:**
- Запуск бота
- Остановка бота

**Сообщения пользователей:**
- User ID, Chat ID
- Текст сообщения
- Команды (/start, /help, /reset)

**Запросы к LLM:**
- Модель
- Размер контекста (количество сообщений)
- Длительность запроса
- Статус (success/error)

**Ошибки:**
- Все исключения с полным stack trace
- Ошибки LLM API с деталями

### Формат лога

```
2025-10-10 14:23:45 | INFO | Bot started
2025-10-10 14:24:10 | INFO | Message from user_id=12345 chat_id=67890: "Привет"
2025-10-10 14:24:11 | INFO | LLM request: model=claude-3.5-sonnet, context_size=3
2025-10-10 14:24:12 | INFO | LLM response: duration=1.2s, status=success
2025-10-10 14:24:15 | ERROR | LLM API error: Connection timeout
```

### Выход логов

- **Файл**: `logs/app.log`
- **Консоль**: stdout (для наблюдения при локальном запуске)

### Настройка в коде

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### Что НЕ используем

- ❌ Структурированное логирование (structlog, loguru)
- ❌ Централизованные системы (ELK Stack, Grafana Loki)
- ❌ Ротация логов (на первом этапе)
- ❌ Логирование в БД
- ❌ Внешние сервисы логирования (Sentry, Rollbar)

---

## 11. Локальный запуск

### Подготовка окружения

1. Установить Python 3.11+
2. Установить Docker и Docker Compose
3. Установить `uv`:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
4. Клонировать репозиторий
5. Создать `.env` файл с обязательными переменными
6. Запустить PostgreSQL через Docker

### Установка зависимостей

```bash
make install
```

Или напрямую через uv:
```bash
uv sync --extra dev
```

### Запуск PostgreSQL

```bash
make db-up
```

Или напрямую:
```bash
docker compose up -d postgres
```

### Применение миграций

```bash
make db-migrate
```

Или напрямую:
```bash
yoyo apply --database "$DATABASE_URL" migrations
```

### Запуск бота

```bash
make run
```

Или напрямую:
```bash
uv run python -m src.main
```

### Остановка бота

- Нажать `Ctrl+C` в терминале

### Makefile команды

```makefile
# Разработка
install:       uv sync --extra dev
run:           uv run python -m src.main

# База данных
db-up:         docker compose up -d postgres
db-down:       docker compose down
db-migrate:    yoyo apply --database "$DATABASE_URL" migrations
db-rollback:   yoyo rollback --database "$DATABASE_URL" migrations

# Тестирование
test:          uv run pytest tests/ -v -m "not integration"
test-cov:      uv run pytest -m "not integration"
test-all:      uv run pytest tests/ -v

# Качество кода
format:        uv run ruff format src/ tests/
lint:          uv run ruff check src/ tests/ && uv run mypy src/ tests/
check-all:     make format && make lint && make test-cov

# Утилиты
clean:         rm -rf logs/*.log htmlcov/ .coverage
```

### Особенности локального запуска

- Бот работает, пока запущен процесс в терминале
- При закрытии терминала - бот останавливается
- История диалогов сохраняется в PostgreSQL между перезапусками
- Логи сохраняются в `logs/app.log` и доступны после перезапуска
- PostgreSQL работает в Docker контейнере

### Требования для запуска

- Python 3.11+
- Docker и Docker Compose
- uv package manager
- PostgreSQL через Docker (автоматически поднимается через `make db-up`)

### Текущий статус деплоя

На текущем этапе деплой на production серверы не предусмотрен:
- ✅ Docker Compose для локальной разработки
- ❌ Без systemd service или process manager
- ❌ Без CI/CD
- ❌ Без облачных платформ
- ✅ Только локальный запуск на машине разработчика

---

