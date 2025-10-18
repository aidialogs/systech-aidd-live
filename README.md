# systech-aidd-live

AI-powered Telegram chatbot с управлением контекстом диалога и интеграцией LLM.

[![Build and Publish](https://github.com/aidialogs/systech-aidd-live/actions/workflows/build-and-publish.yml/badge.svg?branch=day06-smirnov-live-02-ci-pipeline)](https://github.com/aidialogs/systech-aidd-live/actions/workflows/build-and-publish.yml)

![Пример работы бота](doc/day01-preview.png)

## 🎯 Описание

Telegram-бот с искусственным интеллектом, который помнит контекст разговора и может вести осмысленный диалог. Построен по принципу KISS (Keep It Simple, Stupid) - простой, понятный и эффективный код без оверинжиниринга.

## ✨ Возможности

**Telegram Bot:**
- 🤖 **Интеграция с LLM** - подключение к любому OpenAI-compatible API (OpenRouter, OpenAI, и др.)
- 💬 **Управление контекстом** - бот помнит историю диалога с персистентным хранением
- 💾 **База данных** - PostgreSQL для надежного хранения истории диалогов
- ✂️ **Автоматическая обрезка** - контекст ограничен 20 сообщениями для экономии токенов
- 📝 **Команды управления** - `/start`, `/help`, `/reset`, `/role`
- 🗑️ **Soft delete** - логическое удаление данных для возможной аналитики

**Statistics API:**
- 📊 **REST API** - FastAPI для получения статистики диалогов
- 📈 **Дашборд метрик** - статистика по сообщениям, пользователям, активности
- ⏱️ **Временные периоды** - статистика за день/неделю/месяц или за всё время
- 📚 **Автодокументация** - Swagger UI и ReDoc из коробки
- 🔄 **Protocol pattern** - легкая замена Mock → Real реализации

**Общее:**
- 📊 **Полное логирование** - все операции записываются в файл и консоль
- ⚡ **Асинхронная архитектура** - быстрая обработка запросов
- 🧪 **Покрытие тестами** - unit и интеграционные тесты

## Технологии

**Core:**
- Python 3.11+
- aiogram 3.x - асинхронная библиотека для Telegram Bot API
- FastAPI - современный async web framework для REST API
- openai - Python SDK для работы с LLM
- python-dotenv - загрузка переменных окружения
- uv - современный менеджер пакетов

**Database:**
- PostgreSQL 16+ - надежная СУБД для персистентного хранения
- SQLAlchemy 2.0 - async ORM с поддержкой type hints
- asyncpg - высокопроизводительный async драйвер для PostgreSQL
- Alembic - управление миграциями базы данных

**API & Web:**
- FastAPI - REST API с автодокументацией
- Uvicorn - ASGI сервер для FastAPI
- Pydantic - валидация данных и схемы API

**Code Quality:**
- ruff - быстрый линтер и форматтер
- mypy - статическая проверка типов (strict mode)
- pytest - фреймворк для тестирования
- pytest-cov - измерение покрытия кода тестами
- pytest-mock - моки для изоляции тестов
- httpx - HTTP клиент для тестирования API

## Быстрый старт

### 0. Требования

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) - современный менеджер пакетов Python
- Docker + Docker Compose - для запуска PostgreSQL (опционально для dev)

Установка uv:
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# или через pip
pip install uv
```

Установка Docker:
```bash
# macOS
brew install --cask docker

# Или скачайте с https://www.docker.com/products/docker-desktop
```

### 1. Установка зависимостей

```bash
make install
```

Или напрямую через uv:
```bash
uv sync --extra dev
```

Это создаст виртуальное окружение в `.venv/` и установит все зависимости.

### 2. Настройка

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Заполните обязательные переменные:
- `BOT_TOKEN` - токен Telegram бота (получить через @BotFather)
- `LLM_API_KEY` - API ключ OpenRouter
- `LLM_BASE_URL` - URL провайдера LLM
- `LLM_MODEL` - название модели

Опциональные переменные:
- `SYSTEM_PROMPT_FILE` - путь к файлу с системным промптом (по умолчанию используется `prompts/system_prompt.txt`)
- `SYSTEM_PROMPT` - системный промпт (fallback если файл не найден)
- `MAX_CONTEXT_MESSAGES` - максимальное количество сообщений в контексте (по умолчанию 20)
- `DATABASE_URL` - строка подключения к PostgreSQL (см. секцию "База данных")
- `DATABASE_ECHO` - выводить SQL запросы в логи (по умолчанию `False`)

### 3. Запуск

```bash
make run
```

Или напрямую:
```bash
uv run python -m src.main
```

### 4. База данных

Проект использует PostgreSQL для персистентного хранения истории диалогов.

#### Запуск PostgreSQL (через Docker)

```bash
make db-up
```

Это запустит PostgreSQL 16 в Docker контейнере с параметрами из `docker-compose.yml`.

#### Применение миграций

После первого запуска базы данных необходимо применить миграции:

```bash
make db-migrate
```

Это создаст необходимые таблицы в базе данных.

#### Настройка DATABASE_URL

Добавьте в `.env`:
```bash
DATABASE_URL=postgresql+asyncpg://systech_user:systech_password@localhost:5432/systech_aidd
DATABASE_ECHO=False  # True для отладки SQL запросов
```

**Для production используйте безопасный пароль!**

#### Полезные команды для БД

```bash
make db-up              # Запуск PostgreSQL
make db-down            # Остановка PostgreSQL
make db-migrate         # Применить миграции
make db-rollback        # Откатить последнюю миграцию
make db-revision message="название"  # Создать новую миграцию
make db-shell           # Подключиться к PostgreSQL через psql
make db-logs            # Посмотреть логи PostgreSQL
```

#### Структура базы данных

**Таблица `users`:**
- `id` (PK) - Telegram user_id
- `created_at` - дата создания
- `is_deleted` - флаг soft delete

**Таблица `messages`:**
- `id` (PK) - автоинкремент
- `user_id` (FK) - ссылка на user
- `chat_id` - Telegram chat_id
- `role` - роль сообщения (system/user/assistant)
- `content` - текст сообщения
- `content_length` - длина сообщения
- `created_at` - дата создания
- `is_deleted` - флаг soft delete

Подробности см. в [ADR-06: Выбор PostgreSQL + SQLAlchemy](doc/adrs/ADR-06.md).

### 5. Остановка

Нажмите `Ctrl+C` в терминале.

## 🐳 Запуск через Docker

Самый простой способ запустить весь стек сервисов локально одной командой.

### Требования

- Docker Desktop (или Docker Engine + Docker Compose)
- macOS: `brew install --cask docker`
- Или скачайте с https://www.docker.com/products/docker-desktop

### Быстрый старт с Docker

**1. Создайте .env файл**

Скопируйте пример конфигурации:
```bash
cp env.docker.example .env
```

Заполните обязательные переменные:
- `BOT_TOKEN` - токен Telegram бота (получить через @BotFather)
- `LLM_API_KEY` - API ключ OpenRouter
- `LLM_BASE_URL` - URL провайдера LLM
- `LLM_MODEL` - название модели

**Важно:** В Docker окружении `DATABASE_URL` должен использовать хост `postgres` (уже настроено в `env.docker.example`):
```bash
DATABASE_URL=postgresql+asyncpg://systech_user:systech_password@postgres:5432/systech_aidd
```

**2. Запустите все сервисы**

```bash
make docker-up
```

Или напрямую через docker compose:
```bash
docker compose up
```

Это запустит все 4 сервиса:
- **PostgreSQL** - база данных
- **Bot** - Telegram бот
- **API** - REST API сервер
- **Frontend** - веб-интерфейс

**3. Примените миграции БД (только при первом запуске)**

```bash
docker compose exec api uv run alembic upgrade head
```

**4. Проверьте работоспособность**

- **API**: http://localhost:8000/docs - Swagger UI документация
- **Frontend**: http://localhost:3000 - веб-интерфейс
- **Bot**: отправьте сообщение боту в Telegram

Проверить статус всех сервисов:
```bash
make docker-ps
```

**5. Просмотр логов**

```bash
# Все сервисы
make docker-logs

# Только Bot
make docker-logs-bot

# Только API
make docker-logs-api

# Только Frontend
make docker-logs-frontend

# Только PostgreSQL
make docker-logs-db
```

**6. Остановка сервисов**

```bash
make docker-down
```

### Доступные Docker команды

| Команда | Описание |
|---------|----------|
| `make docker-up` | Запуск всех сервисов (detached mode) |
| `make docker-down` | Остановка всех сервисов |
| `make docker-build` | Пересборка Docker образов (no cache) |
| `make docker-logs` | Просмотр логов всех сервисов |
| `make docker-logs-bot` | Просмотр логов Bot |
| `make docker-logs-api` | Просмотр логов API |
| `make docker-logs-frontend` | Просмотр логов Frontend |
| `make docker-logs-db` | Просмотр логов PostgreSQL |
| `make docker-ps` | Показать статус всех сервисов |
| `make docker-restart` | Перезапуск всех сервисов |
| `make docker-clean` | Полная очистка (containers + volumes + images) |

### Структура сервисов

```
┌─────────────┐
│  Frontend   │ :3000
│  (Next.js)  │
└──────┬──────┘
       │
       ↓
┌─────────────┐     ┌─────────────┐
│     API     │←────│     Bot     │
│  (FastAPI)  │:8000│  (aiogram)  │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └───────┬───────────┘
               ↓
       ┌─────────────┐
       │ PostgreSQL  │ :5432
       └─────────────┘
```

### Полезные советы

**Пересборка образов после изменений кода:**
```bash
make docker-build
make docker-up
```

**Просмотр логов в реальном времени:**
```bash
docker compose logs -f api bot
```

**Подключение к PostgreSQL:**
```bash
docker compose exec postgres psql -U systech_user -d systech_aidd
```

**Выполнение команд внутри контейнера:**
```bash
# Запуск тестов в API контейнере
docker compose exec api uv run pytest

# Проверка версии Python
docker compose exec bot python --version
```

## 📚 Руководства для разработчиков

Для полного понимания проекта создан набор подробных гайдов:

- **[GUIDE-01: Getting Started](doc/guides/01-getting-started.md)** — запустить бота за 15 минут
- **[GUIDE-02: Архитектура](doc/guides/02-architecture.md)** — понять структуру системы
- **[GUIDE-03: Визуальный обзор](doc/guides/03-visual-overview.md)** — 26 диаграмм по SDLC
- **[GUIDE-06: Codebase Tour](doc/guides/06-codebase-tour.md)** — детальный обзор всех файлов
- **[GUIDE-07: Development Workflow](doc/guides/07-development-workflow.md)** — процесс разработки
- **[GUIDE-08: Testing](doc/guides/08-testing.md)** — стратегия тестирования

**➡️ [Полный список гайдов](doc/guides/README.md)**

Рекомендуется пройти гайды последовательно (3-4 часа).

## 🔧 Настройка окружения

### VSCode

Проект настроен для работы с VSCode через `uv`. После установки зависимостей:

1. Откройте проект в VSCode
2. VSCode автоматически определит интерпретатор из `.venv/`
3. Все настройки уже сконфигурированы в `.vscode/`:
   - `settings.json` - настройки Python, ruff, mypy, pytest
   - `launch.json` - конфигурации отладки (Run Bot, Run Tests, etc.)
   - `tasks.json` - задачи для запуска команд через uv
   - `extensions.json` - рекомендуемые расширения

**Рекомендуемые расширения VSCode:**
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Ruff (charliermarsh.ruff)
- Python Debugger (ms-python.debugpy)

VSCode предложит установить их автоматически при открытии проекта.

**Доступные конфигурации запуска (F5):**
- `Python: Run Bot` - запуск бота с отладкой
- `Python: Run All Tests` - запуск всех тестов (unit + integration)
- `Python: Run Tests (No Integration)` - только unit-тесты (быстро)
- `Python: Run Integration Tests Only` - только integration тесты (реальные API вызовы)
- `Python: Run Tests with Coverage` - тесты с coverage (без integration)
- `Python: Debug Current Test File` - отладка текущего файла тестов

**Доступные задачи (Cmd+Shift+P > Tasks: Run Task):**
- `Install Dependencies` - установка зависимостей через uv
- `Run Bot` - запуск бота
- `Run Tests` - запуск unit тестов
- `Run Tests (No Integration)` - только unit тесты
- `Run Tests with Coverage` - тесты с coverage отчётом
- `Run Integration Tests` - только integration тесты
- `Format Code` - форматирование кода
- `Lint Code` - проверка кода
- `Check All` - полная проверка (format + lint + test)
- `Clean Build Artifacts` - очистка временных файлов

### Терминал

Все команды в проекте должны запускаться через `uv run`:

```bash
# ❌ Неправильно
python -m pytest
pytest tests/

# ✅ Правильно
uv run pytest tests/
make test
```

Это гарантирует, что используется правильное виртуальное окружение со всеми зависимостями.

## Команды

**Разработка:**
- `make install` - установка зависимостей (включая dev-инструменты)
- `make run` - запуск бота

**API (Statistics Dashboard):**
- `make api-run` - запуск API сервера
- `make api-test` - тестирование API endpoints (curl)
- `make api-docs` - открыть Swagger UI документацию

**Тестирование:**
- `make test` - запуск unit тестов (без integration)
- `make test-cov` - запуск тестов с измерением coverage (без integration)
- `make test-integration` - запуск только интеграционных тестов (реальные вызовы LLM)
- `make test-all` - запуск всех тестов (unit + integration)

**Качество кода:**
- `make format` - автоформатирование кода (ruff format)
- `make lint` - проверка кода (ruff check + mypy)
- `make check-all` - полная проверка (format + lint + test-cov)

**Утилиты:**
- `make clean` - очистка логов и отчетов coverage

## 🤖 Команды бота

- `/start` - начать работу с ботом (приветствие)
- `/help` - показать справку с описанием команд
- `/reset` - очистить историю диалога и начать сначала
- `/role` - показать информацию о роли ассистента (AICodingExpert)

## 💡 Пример использования

1. Напишите боту: **"Меня зовут Сергей"**
   - Бот: *"Приятно познакомиться, Сергей!"*

2. Напишите: **"Как меня зовут?"**
   - Бот: *"Вас зовут Сергей"* (помнит предыдущий контекст!)

3. Напишите: **`/reset`**
   - Бот: *"История диалога очищена. Начнем сначала!"*

4. Напишите снова: **"Как меня зовут?"**
   - Бот: *"Я не знаю, как вас зовут..."* (контекст очищен)

## 📊 Statistics API

REST API для получения статистики по диалогам. Предназначен для интеграции с frontend дашбордом.

### Запуск API

```bash
# Запустить API сервер
make api-run

# API будет доступен на http://localhost:8000
# Swagger UI: http://localhost:8000/docs
```

### Основной endpoint

```bash
GET /api/v1/statistics?period={day|week|month|all}
```

**Параметры:**
- `period` (optional) - период статистики: `day`, `week`, `month` (default), `all`

**Пример запроса:**
```bash
curl "http://localhost:8000/api/v1/statistics?period=week"
```

**Ответ включает:**
- **overview** - общая статистика (количество сообщений, пользователей, чатов, средняя длина)
- **messages_by_role** - распределение по ролям (user, assistant, system)
- **messages_over_time** - временной ряд (почасовая/дневная/месячная статистика)
- **top_metrics** - ключевые показатели (активные пользователи, сообщения за период)

### Документация

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Примеры**: [doc/api-examples.md](doc/api-examples.md)

### Текущая реализация

На данный момент используется **MockStatCollector** с генерацией тестовых данных. В Sprint S5 будет добавлена реальная реализация с подключением к PostgreSQL.

## 🎨 Frontend Dashboard

Modern web interface for statistics dashboard and admin chat.

### Tech Stack

- Next.js 15 (App Router) + TypeScript + shadcn/ui + Tailwind CSS

### Quick Start

```bash
# Install frontend dependencies
make frontend-install

# Start development server
make frontend-dev

# Open http://localhost:3000
```

### Commands

```bash
make frontend-dev            # Start dev server
make frontend-build          # Production build
make frontend-lint           # Lint code
make frontend-format         # Format code
make frontend-type-check     # TypeScript check
make frontend-check-all      # All checks
```

See [frontend/README.md](frontend/README.md) for details.

## 🔧 DevOps & Infrastructure

DevOps infrastructure for containerization, CI/CD, and automated deployment.

### Quick Links

- 📋 [DevOps Roadmap](devops/doc/devops-roadmap.md) - development roadmap for DevOps processes
- 🐳 **Docker containerization** - ✅ **Готово!** Запуск всех сервисов: `make docker-up`
- 📝 [Docker Setup Summary](DOCKER-SETUP-SUMMARY.md) - краткое руководство по Docker
- 🔄 **GitHub Actions** - ✅ **Готово!** Автоматическая сборка и публикация образов
- 🚀 Auto Deploy - one-click deployment to production server (планируется в D3)

### Current Status

**Sprint D0: Basic Docker Setup** - ✅ Выполнен

- Созданы Dockerfile для всех сервисов (bot, api, frontend)
- Настроен docker-compose.yml для оркестрации
- Добавлены удобные команды в Makefile
- Обновлена документация с инструкциями

**Sprint D1: Build & Publish** - ✅ Выполнен

- GitHub Actions workflow для автоматической сборки образов
- Публикация в GitHub Container Registry (ghcr.io)
- Публичные образы доступны без авторизации
- docker-compose.prod.yml для использования образов из registry

**Следующий шаг:** Sprint D2 - Развертывание на сервер (ручной deploy)

См. [DevOps Roadmap](devops/doc/devops-roadmap.md) для детального плана.

### Services Architecture

```
Frontend (Next.js + pnpm) :3000
    ↓
API (FastAPI + UV) :8000 ← Bot (Python + UV + aiogram)
    ↓
PostgreSQL :5432
```

**Все сервисы в Docker:**
- ✅ Запуск одной командой: `make docker-up`
- ✅ Логи: `make docker-logs`
- ✅ Статус: `make docker-ps`

См. [DOCKER-SETUP-SUMMARY.md](DOCKER-SETUP-SUMMARY.md) для быстрого старта.

## 🚢 Использование образов из GitHub Container Registry

Образы автоматически публикуются в ghcr.io после каждого commit в ветку `day06-smirnov-live-02-ci-pipeline`.

### Быстрый старт с готовыми образами

**1. Создайте .env файл:**
```bash
cp env.docker.example .env
# Заполните обязательные переменные (BOT_TOKEN, LLM_API_KEY, etc.)
```

**2. Скачайте образы из registry:**
```bash
make docker-pull
```

**3. Запустите сервисы:**
```bash
make docker-prod-up
```

**4. Примените миграции (только при первом запуске):**
```bash
docker compose -f docker-compose.prod.yml exec api uv run alembic upgrade head
```

**5. Проверьте работоспособность:**
- API: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Bot: отправьте сообщение боту в Telegram

### Доступные образы

Все образы публичные - авторизация не требуется:

- `ghcr.io/aidialogs/systech-aidd-bot:latest` - Telegram bot
- `ghcr.io/aidialogs/systech-aidd-api:latest` - REST API
- `ghcr.io/aidialogs/systech-aidd-frontend:latest` - Web UI

### Команды для работы с registry образами

| Команда | Описание |
|---------|----------|
| `make docker-pull` | Скачать образы из registry |
| `make docker-prod-up` | Запуск с образами из registry |
| `make docker-prod-down` | Остановка prod окружения |
| `make docker-prod-logs` | Просмотр логов |
| `make docker-prod-ps` | Статус сервисов |
| `make docker-prod-restart` | Перезапуск сервисов |

### Локальная разработка vs Production образы

**Локальная разработка (сборка образов локально):**
```bash
make docker-build    # Собрать образы
make docker-up       # Запустить сервисы
make docker-logs     # Просмотр логов
```

**Production образы (из registry):**
```bash
make docker-pull        # Скачать образы из ghcr.io
make docker-prod-up     # Запустить с образами из registry
make docker-prod-logs   # Просмотр логов
```

### Версионирование образов

Каждый образ имеет два тега:
- `latest` - последняя версия из ветки
- `sha-<commit>` - конкретная версия по commit hash

**Пример использования конкретной версии:**
```bash
docker pull ghcr.io/aidialogs/systech-aidd-bot:sha-a1b2c3d4
```

## Структура проекта

```
systech-aidd-live/
├── src/                    # Исходный код
│   ├── __init__.py
│   ├── main.py            # Точка входа бота
│   ├── api_server.py      # Точка входа API
│   ├── config.py          # Конфигурация (dataclass)
│   ├── exceptions.py      # Кастомные исключения
│   ├── protocols.py       # Протоколы для DI
│   ├── message.py         # Класс Message
│   ├── command_handler.py # Обработка команд (/start, /help, /reset, /role)
│   ├── message_handler.py # Координация обработки сообщений
│   ├── llm_client.py      # Работа с LLM API
│   ├── context_manager.py # Управление контекстом
│   ├── models.py          # SQLAlchemy модели
│   ├── database.py        # Async DB lifecycle
│   ├── repository.py      # Repository pattern для БД
│   └── api/               # API модули
│       ├── __init__.py
│       ├── main.py        # FastAPI приложение
│       ├── protocols.py   # StatCollectorProtocol
│       ├── schemas.py     # Pydantic модели
│       └── stat_collector_mock.py  # Mock реализация
├── prompts/               # Системные промпты
│   └── system_prompt.txt  # Промпт AICodingExpert
├── tests/                 # Тесты
│   ├── conftest.py        # Фикстуры pytest
│   ├── test_*.py          # Unit тесты для каждого модуля
│   ├── test_api_mock.py   # Тесты API
│   └── test_integration.py # Интеграционные тесты
├── logs/                  # Логи
├── doc/                   # Документация
│   ├── vision.md          # Техническое видение
│   ├── api-examples.md    # Примеры использования API
│   ├── roadmap.md         # Roadmap разработки
│   └── adrs/              # Architecture Decision Records
├── frontend/              # Frontend (в разработке)
│   └── doc/
│       ├── frontend-roadmap.md  # Roadmap frontend
│       └── plans/
│           └── s1-mock-api-plan.md  # План Sprint S1
├── devops/                # DevOps инфраструктура
│   ├── README.md          # DevOps документация
│   └── doc/
│       ├── devops-roadmap.md  # Roadmap DevOps процессов
│       └── plans/         # Планы спринтов
├── .env                   # Конфигурация (не в git)
├── .env.example           # Пример конфигурации
├── pyproject.toml         # Зависимости + конфигурация инструментов
├── Makefile               # Команды автоматизации
└── README.md
```

## 🏗️ Архитектурные особенности

**Принципы:**
- **SOLID** - Single Responsibility (CommandHandler), Dependency Inversion (Protocols)
- **DRY** - нет дублирования кода
- **KISS** - простота без оверинжиниринга
- **Type Safety** - 100% type hints, mypy strict mode

**Реализация:**
- **Один класс = один файл** - строгое правило для читаемости
- **Асинхронный код** - async/await везде (aiogram + AsyncOpenAI)
- **Плоская структура** - все в `src/` без глубокой вложенности
- **Dependency Injection** - через Protocols для тестируемости
- **Custom Exceptions** - `ConfigError`, `LLMError` для явной обработки ошибок
- **In-memory хранение** - контекст в памяти, без БД на этапе MVP

## 📊 Логирование

Формат логов: `YYYY-MM-DD HH:MM:SS | LEVEL | message`

Логируется:
- Запуск/остановка бота
- Входящие сообщения (user_id, chat_id, текст)
- Команды (`/start`, `/help`, `/reset`)
- LLM запросы (модель, размер контекста, длительность)
- Создание/обрезка/очистка контекста
- Ошибки с деталями

Логи сохраняются в `logs/app.log` и выводятся в консоль.

## 🧪 Тестирование

Проект покрыт comprehensive test suite с **100% code coverage**:

```bash
make test              # Unit тесты (быстро, ~2.8s)
make test-cov          # Unit тесты с coverage report
make test-integration  # Только integration тесты (реальные API вызовы)
make test-all          # Все тесты включая integration (~4.5s)
```

**30 тестов:**
- `test_message.py` (4 теста) - класс Message
- `test_config.py` (5 тестов) - валидация конфигурации
- `test_command_handler.py` (6 тестов) - обработка команд
- `test_message_handler.py` (7 тестов) - координация с моками
- `test_llm_client.py` (4 теста) - LLM клиент + error handling (3 unit + 1 integration)
- `test_context_manager.py` (3 теста) - управление контекстом
- `test_integration.py` (1 тест) - интеграционный тест обрезки контекста

**Подход:**
- Fixtures в `conftest.py` для переиспользования (включая `clean_env` для изоляции окружения)
- Моки (`AsyncMock`, `Mock`) для изоляции unit тестов
- Integration tests помечены маркером `@pytest.mark.integration`
- Integration тесты делают реальные вызовы к LLM API
- 100% statement coverage для всех модулей

## 📈 Статистика

- **19 Python файлов** (10 src + 9 tests)
- **30/30 тестов проходят** ✅
- **100% code coverage** ✅
- **0 mypy errors** (strict mode) ✅
- **0 ruff warnings** ✅
- **8 итераций разработки** (MVP + устранение технического долга)

## 🎯 Качество кода

Проект следует строгим стандартам качества:

**Метрики:**
- ✅ Test Coverage: 100% (165/165 statements)
- ✅ Type Hints: 100% всех функций и методов
- ✅ Mypy: strict mode, 0 errors
- ✅ Ruff: 0 warnings (E, F, I, N, UP, ANN, B, A, C4, DTZ, PIE, PT, RET, SIM, ARG, ERA, RUF)

**Инструменты:**
```bash
make format    # Ruff форматирование
make lint      # Ruff + Mypy проверка
make check-all # Полная проверка (format + lint + test-cov)
```

**Подход:**
- Итеративное устранение технического долга
- ADR (Architecture Decision Records) для важных решений  
- Continuous refactoring с зелеными тестами
- Development workflow с автоматическими проверками

## 📚 Документация

Подробная документация находится в каталоге `doc/`:
- **`guides/`** - 6 подробных гайдов для онбординга и разработки ([полный список](doc/guides/README.md))
- `vision.md` - техническое видение проекта
- `tasklist.md` - итерационный план разработки с отчетом по прогрессу
- `adrs/` - Architecture Decision Records

## 🚀 Разработка

Проект разработан итеративно за **8 итераций**:

**MVP (Итерации 0-4):**
0. **Эхо-бот** - базовая инфраструктура
1. **Интеграция LLM** - подключение OpenAI API
2. **История диалога** - сохранение контекста
3. **Команды и обрезка** - управление контекстом
4. **Финальное тестирование** - проверка сценариев

**Устранение технического долга (Итерации 0-3):**
0. **Инструменты качества** - ruff, mypy, pytest-cov, Makefile
1. **Type hints + валидация** - dataclass Config, custom exceptions
2. **Архитектурный рефакторинг** - SOLID, DRY, Protocols, CommandHandler
3. **Улучшение тестирования** - 100% coverage, fixtures, моки
4. **Финальная проверка** - документация, ADR, метрики

Каждая итерация закоммичена в git с подробным описанием.

**Development Workflow:**
1. Написать код → `make format`
2. Проверить качество → `make lint`
3. Запустить тесты → `make test-cov`
4. Проверить все → `make check-all`
5. Закоммитить изменения

## 🤝 Вклад

Проект создан в рамках курса **SYSTECH-AIDD-2025**.

## 📄 Лицензия

MIT


