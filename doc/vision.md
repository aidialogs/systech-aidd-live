# Техническое видение проекта

## 1. Технологии

### Основной стек
- **Python 3.11+** - базовый язык разработки
- **aiogram 3.x** - асинхронная библиотека для Telegram Bot API
- **openai** - Python SDK для работы с LLM через OpenAI Compatible API
- **python-dotenv** - загрузка переменных окружения из .env файла

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

### Деплой
- **Локальный запуск** - `python -m src.main`
- Без Docker на первом этапе
- Запуск вручную, без автоматизации CI/CD

---

## 2. Принципы разработки

### Ключевые принципы
- **KISS (Keep It Simple, Stupid)** - никакого оверинжиниринга, только необходимое для проверки идеи
- **Один класс = один файл** - строгое правило для структурированности кода
- **Явное лучше неявного** - простой и понятный код
- **Asyncio** - асинхронный код (т.к. aiogram и openai async)

### Что НЕ используем (для простоты MVP)
- ❌ Сложные паттерны проектирования (фабрики, строители, стратегии)
- ❌ DI-контейнеры и IoC
- ❌ Избыточную абстракцию и многоуровневую иерархию классов
- ❌ Pydantic models (используем простые dataclasses)
- ❌ Микросервисы
- ❌ Очереди сообщений
- ❌ БД на первом этапе (только in-memory хранение контекста)

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
│   ├── message.py           # Message класс - структура сообщения
│   ├── message_handler.py   # MessageHandler класс - обработка сообщений
│   ├── llm_client.py        # LLMClient класс - работа с LLM API
│   └── context_manager.py   # ContextManager класс - управление контекстом
├── tests/
│   ├── __init__.py
│   ├── test_llm_client.py
│   └── test_context_manager.py
├── logs/                    # Директория для логов (создается автоматически)
│   └── app.log
├── .env.example             # Пример конфигурации
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
     ↓          ↓
[ContextManager] [LLMClient]
     ↓              ↓
[In-Memory Dict]  [OpenAI API]
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
- Оркестрирует взаимодействие между ContextManager и LLMClient
- Обрабатывает команды: /start, /help, /reset
- Обработка ошибок с дружелюбными сообщениями

**ContextManager** (хранилище):
- Хранит историю диалогов в памяти (dict: (user_id, chat_id) → list of Message)
- Ограничение контекста: последние N сообщений (например, 20)
- Очистка контекста по команде

**LLMClient** (клиент внешнего API):
- Отправка запросов к OpenAI Compatible API
- Формирование запросов в формате chat completion
- Возврат текста ответа или exception при ошибке

**Config** (конфигурация):
- Загрузка параметров из .env с валидацией
- Dataclass со строгой типизацией
- Валидация обязательных переменных при старте (Config.from_env())
- Бросает ConfigError если отсутствуют обязательные переменные
- Хранение: bot_token, llm_api_key, llm_base_url, llm_model, system_prompt, max_context_messages

### Принципы архитектуры
- **Простота** - минимум слоев и абстракций
- **Синхронность операций** - последовательная обработка без очередей
- **In-memory state** - без БД, состояние в памяти процесса
- **Stateless LLM** - LLMClient не хранит состояние

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

### Структура хранилища контекста

```python
# ContextManager.contexts
{
    (user_id, chat_id): [
        Message("system", "Ты полезный ассистент..."),
        Message("user", "Привет"),
        Message("assistant", "Здравствуйте!"),
        ...
    ]
}
```

**Ключ хранилища:**
- `(user_id, chat_id)` - кортеж из двух int
- `user_id` - ID пользователя из Telegram (message.from_user.id)
- `chat_id` - ID чата из Telegram (message.chat.id)

**Значение:**
- Список объектов Message

### Ограничения и правила

- **max_context_messages**: 20 сообщений (настраивается через Config)
- При превышении лимита - удаляются старые сообщения (кроме system)
- System prompt всегда остается первым в списке
- Хранение только в оперативной памяти (при перезапуске - потеря данных)

### Без использования:
- ❌ Базы данных (PostgreSQL, SQLite)
- ❌ ORM (SQLAlchemy)
- ❌ Персистентное хранилище
- ❌ Pydantic models (используем простые dataclasses)

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

**4. Сброс контекста - команда /reset**
- Пользователь отправляет `/reset`
- ContextManager очищает историю диалога для (user_id, chat_id)
- Бот подтверждает: "История диалога очищена. Начнем сначала!"

**5. Обработка ошибок LLM API**
- При ошибке API (timeout, недоступность сервиса, etc.)
- MessageHandler перехватывает exception
- Пользователь видит дружелюбное сообщение:
  - "Извините, не могу ответить прямо сейчас. Попробуйте чуть позже."
- Ошибка логируется для последующего анализа

**6. Длинный диалог (превышение лимита контекста)**
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
        ...
```

### Параметры конфигурации

**Обязательные параметры:**
- `BOT_TOKEN` - токен Telegram бота (получить через @BotFather)
- `LLM_API_KEY` - API ключ для OpenRouter
- `LLM_BASE_URL` - URL провайдера LLM (https://openrouter.ai/api/v1)
- `LLM_MODEL` - название модели (например: anthropic/claude-3.5-sonnet)

**Опциональные параметры (с дефолтами):**
- `SYSTEM_PROMPT` - системный промпт (default: "Ты полезный AI-ассистент")
- `MAX_CONTEXT_MESSAGES` - лимит сообщений в контексте (default: 20)

### Файлы конфигурации

**.env** (не в git):
```bash
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
LLM_API_KEY=sk-or-v1-xxxxxxxxxxxxx
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet
SYSTEM_PROMPT=Ты полезный AI-ассистент. Отвечай кратко и по делу.
MAX_CONTEXT_MESSAGES=20
```

**.env.example** (в git):
```bash
BOT_TOKEN=your_telegram_bot_token
LLM_API_KEY=your_openrouter_api_key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet
SYSTEM_PROMPT=Ты полезный AI-ассистент
MAX_CONTEXT_MESSAGES=20
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
2. Установить `uv`:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Клонировать репозиторий
4. Создать `.env` файл на основе `.env.example`
5. Заполнить обязательные переменные в `.env`

### Установка зависимостей

```bash
make install
```

Или напрямую через uv:
```bash
uv sync
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
install:
    uv sync --extra dev

run:
    uv run python -m src.main

test:
    uv run pytest

test-cov:
    uv run pytest  # с coverage (настроено в pyproject.toml)

format:
    uv run ruff format src/ tests/

lint:
    uv run ruff check src/ tests/
    uv run mypy src/ tests/

check-all:
    make format && make lint && make test-cov

clean:
    rm -rf logs/*.log htmlcov/ .coverage
```

### Особенности локального запуска

- Бот работает, пока запущен процесс в терминале
- При закрытии терминала - бот останавливается
- При перезапуске - вся история диалогов теряется (in-memory storage)
- Логи сохраняются в `logs/app.log` и доступны после перезапуска

### Без деплоя на серверы

На этапе MVP деплой не предусмотрен:
- ❌ Без Docker / docker-compose
- ❌ Без systemd service или process manager
- ❌ Без CI/CD
- ❌ Без облачных платформ
- ❌ Только локальный запуск на машине разработчика

---

