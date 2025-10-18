# systech-aidd-live

AI-powered Telegram chatbot с управлением контекстом диалога и интеграцией LLM.

![Пример работы бота](doc/day01-preview.png)

## 🎯 Описание

Telegram-бот с искусственным интеллектом, который помнит контекст разговора и может вести осмысленный диалог. Построен по принципу KISS (Keep It Simple, Stupid) - простой, понятный и эффективный код без оверинжиниринга.

## ✨ Возможности

- 🤖 **Интеграция с LLM** - подключение к любому OpenAI-compatible API (OpenRouter, OpenAI, и др.)
- 💬 **Управление контекстом** - бот помнит историю диалога с персистентным хранением
- 💾 **База данных** - PostgreSQL для надежного хранения истории диалогов
- ✂️ **Автоматическая обрезка** - контекст ограничен 20 сообщениями для экономии токенов
- 📝 **Команды управления** - `/start`, `/help`, `/reset`, `/role`
- 🗑️ **Soft delete** - логическое удаление данных для возможной аналитики
- 📊 **Полное логирование** - все операции записываются в файл и консоль
- ⚡ **Асинхронная архитектура** - быстрая обработка запросов
- 🧪 **Покрытие тестами** - unit и интеграционные тесты (81%+ coverage)

## Технологии

**Core:**
- Python 3.11+
- aiogram 3.x - асинхронная библиотека для Telegram Bot API
- openai - Python SDK для работы с LLM
- python-dotenv - загрузка переменных окружения
- uv - современный менеджер пакетов

**Database:**
- PostgreSQL 16+ - надежная СУБД для персистентного хранения
- SQLAlchemy 2.0 - async ORM с поддержкой type hints
- asyncpg - высокопроизводительный async драйвер для PostgreSQL
- Alembic - управление миграциями базы данных

**Code Quality:**
- ruff - быстрый линтер и форматтер
- mypy - статическая проверка типов (strict mode)
- pytest - фреймворк для тестирования
- pytest-cov - измерение покрытия кода тестами
- pytest-mock - моки для изоляции тестов

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

## 🐳 Запуск через Docker (рекомендуется)

**Самый простой способ запустить весь проект локально одной командой!**

Docker автоматически запустит все необходимые сервисы:
- PostgreSQL база данных
- Telegram бот
- FastAPI сервер
- Next.js frontend

### Требования

- Docker 20.10+ и Docker Compose 2.0+
- Около 2 GB свободного места

### Быстрый запуск

```bash
# 1. Создайте файл .env из шаблона
cp devops/env.example .env

# 2. Отредактируйте .env и заполните BOT_TOKEN, LLM_API_KEY и другие переменные
nano .env

# 3. Запустите все сервисы
cd devops
docker compose up
```

Готово! 🎉

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000/docs
- **Bot**: работает в Telegram

### Подробная документация

Полный гайд по Docker см. в [devops/doc/DOCKER_QUICKSTART.md](devops/doc/DOCKER_QUICKSTART.md)

---

## Локальная разработка (без Docker)

Если вы хотите запустить проект локально для разработки без Docker:

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

## Структура проекта

```
systech-aidd-live/
├── src/                    # Исходный код
│   ├── __init__.py
│   ├── main.py            # Точка входа
│   ├── config.py          # Конфигурация (dataclass)
│   ├── exceptions.py      # Кастомные исключения
│   ├── protocols.py       # Протоколы для DI
│   ├── message.py         # Класс Message
│   ├── command_handler.py # Обработка команд (/start, /help, /reset, /role)
│   ├── message_handler.py # Координация обработки сообщений
│   ├── llm_client.py      # Работа с LLM API
│   └── context_manager.py # Управление контекстом
├── prompts/               # Системные промпты
│   └── system_prompt.txt  # Промпт AICodingExpert
├── tests/                 # Тесты (100% coverage)
│   ├── conftest.py        # Фикстуры pytest
│   ├── test_*.py          # Unit тесты для каждого модуля
│   └── test_integration.py # Интеграционные тесты
├── logs/                  # Логи
├── doc/                   # Документация
│   ├── vision.md          # Техническое видение
│   ├── tasklist.md        # План разработки MVP
│   ├── tasklist_tech_debt.md # План устранения технического долга
│   └── adrs/              # Architecture Decision Records
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


