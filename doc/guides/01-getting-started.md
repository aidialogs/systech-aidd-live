# GUIDE-01: Getting Started

**Цель**: За 15 минут запустить бота локально и отправить первое сообщение.

---

## Prerequisites

Перед началом убедитесь, что установлено:

- **Python 3.11+** — проверьте версию: `python --version`
- **uv** — современный менеджер пакетов Python
- **Docker + Docker Compose** — для запуска PostgreSQL (обязательно)

### Установка uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# или через pip
pip install uv
```

После установки перезапустите терминал и проверьте: `uv --version`

### Установка Docker

```bash
# macOS
brew install --cask docker

# Или скачайте Docker Desktop с https://www.docker.com/products/docker-desktop
```

Запустите Docker Desktop и убедитесь, что Docker работает: `docker --version`

---

## Шаг 1: Клонирование репозитория

```bash
cd ~/projects  # или ваша рабочая директория
git clone <repository-url> systech-aidd-live
cd systech-aidd-live
```

---

## Шаг 2: Установка зависимостей

```bash
make install
```

Эта команда:
- Создаст виртуальное окружение в `.venv/`
- Установит все зависимости из `pyproject.toml` и `uv.lock`
- Установит dev-инструменты (pytest, ruff, mypy)

**Время**: ~30-60 секунд

---

## Шаг 3: Получение токенов

### 3.1 Telegram Bot Token

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям (имя бота и username)
4. Получите токен формата `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### 3.2 LLM API Key (OpenRouter)

1. Зайдите на [openrouter.ai](https://openrouter.ai)
2. Зарегистрируйтесь или войдите
3. Перейдите в Keys → Create Key
4. Получите ключ формата `sk-or-v1-xxxxxxxxxxxxx`

---

## Шаг 4: Настройка .env

Создайте файл `.env` на основе примера:

```bash
cp .env.example .env
```

Откройте `.env` и заполните:

```bash
# Telegram Bot
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# LLM API
LLM_API_KEY=sk-or-v1-xxxxxxxxxxxxx
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet

# База данных PostgreSQL
DATABASE_URL=postgresql+asyncpg://systech_user:systech_password@localhost:5432/systech_aidd
DATABASE_ECHO=False

# Опциональные (можно оставить как есть)
SYSTEM_PROMPT_FILE=prompts/system_prompt.txt
MAX_CONTEXT_MESSAGES=20
```

**Важно**: Файл `.env` НЕ должен попадать в git (уже в `.gitignore`).

---

## Шаг 5: Запуск базы данных

Проект использует PostgreSQL для хранения истории диалогов.

### 5.1 Запуск PostgreSQL

```bash
make db-up
```

Эта команда запустит PostgreSQL 16 в Docker контейнере. Вы увидите:

```
[+] Running 2/2
 ✔ Network systech-aidd-live_default    Created
 ✔ Container systech-aidd-postgres      Started
```

### 5.2 Применение миграций

После первого запуска базы данных необходимо создать таблицы:

```bash
make db-migrate
```

Вы увидите:

```
INFO  [alembic.runtime.migration] Running upgrade -> 09eb92e9cbfc, create users and messages tables
```

**Готово!** База данных настроена и готова к работе.

---

## Шаг 6: Запуск бота

```bash
make run
```

Вы должны увидеть:

```
2025-10-16 14:23:45 | INFO | System prompt loaded from file: prompts/system_prompt.txt
2025-10-16 14:23:45 | INFO | Database initialized
2025-10-16 14:23:45 | INFO | Bot started
```

Бот работает! Оставьте терминал открытым.

---

## Шаг 7: Тестирование

1. Откройте Telegram
2. Найдите вашего бота по username (который создали в @BotFather)
3. Отправьте `/start`

Бот ответит:
```
Привет! Я AI-ассистент. Используй /help для справки.
```

4. Попробуйте задать вопрос: "Что такое Python?"

Бот ответит на основе LLM.

5. Отправьте `/help` — увидите список команд:
   - `/start` — Начать диалог
   - `/help` — Показать справку
   - `/reset` — Очистить историю диалога
   - `/role` — Показать информацию о роли ассистента

---

## Шаг 8: Остановка бота и БД

### Остановка бота

В терминале нажмите **Ctrl+C**

Вы увидите:
```
2025-10-16 14:25:30 | INFO | Closing database connections
2025-10-16 14:25:30 | INFO | Bot stopped
```

### Остановка PostgreSQL (опционально)

Если хотите остановить базу данных:

```bash
make db-down
```

---

## Проверка работы контекста

Давайте проверим, что бот помнит историю диалога:

1. Запустите бота: `make run`
2. Напишите боту: **"Меня зовут Сергей"**
3. Бот ответит что-то вроде: *"Приятно познакомиться, Сергей!"*
4. Напишите: **"Как меня зовут?"**
5. Бот ответит: *"Вас зовут Сергей"* ✅ (помнит контекст!)
6. Отправьте `/reset`
7. Снова напишите: **"Как меня зовут?"**
8. Бот ответит: *"Я не знаю, как вас зовут..."* ✅ (контекст очищен)

**Важно**: Теперь контекст сохраняется в PostgreSQL. Даже если вы перезапустите бота, история диалога сохранится (до вызова `/reset`)!

---

## Troubleshooting

### ❌ "Command not found: uv"
```bash
# Переустановите uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# Перезапустите терминал
```

### ❌ "Command not found: docker"
```bash
# macOS
brew install --cask docker

# Или скачайте Docker Desktop с https://www.docker.com/products/docker-desktop
# Запустите Docker Desktop
```

### ❌ "Missing required environment variables: BOT_TOKEN"
Проверьте:
1. Файл `.env` создан
2. В `.env` заполнены все обязательные поля
3. Нет лишних пробелов в `.env`

### ❌ "LLM API error: Unauthorized"
Проверьте:
1. `LLM_API_KEY` правильный
2. На OpenRouter есть баланс или free credits

### ❌ "Error: port is already allocated" (база данных)
База данных уже запущена или порт 5432 занят:
```bash
# Проверьте запущена ли БД
docker ps | grep postgres

# Остановите старый контейнер
make db-down

# Запустите снова
make db-up
```

### ❌ "Database connection failed"
Проверьте:
1. PostgreSQL запущен: `make db-up`
2. `DATABASE_URL` правильный в `.env`
3. Миграции применены: `make db-migrate`

### ❌ Бот не отвечает в Telegram
1. Убедитесь, что бот запущен (терминал с `make run`)
2. Проверьте, что `BOT_TOKEN` правильный (нет лишних символов)
3. Проверьте, что база данных запущена: `docker ps | grep postgres`
4. Попробуйте `/start` — если не отвечает, пересоздайте бота через @BotFather

---

## Что дальше?

✅ Бот запущен и работает!

Переходите к следующим гайдам:
- **GUIDE-02**: Архитектура проекта — как устроена система (бот, БД, API, frontend)
- **GUIDE-06**: Codebase Tour — обзор всех файлов
- **GUIDE-07**: Development Workflow — как добавлять новые фичи
- **GUIDE-08**: Testing — как писать и запускать тесты

---

## Полезные команды

**Бот:**
```bash
make run              # Запуск бота
```

**База данных:**
```bash
make db-up            # Запуск PostgreSQL
make db-down          # Остановка PostgreSQL
make db-migrate       # Применить миграции
make db-shell         # Подключиться к PostgreSQL (psql)
make db-logs          # Посмотреть логи БД
```

**API (опционально):**
```bash
make api-run          # Запуск API сервера (http://localhost:8000)
make api-docs         # Открыть Swagger UI документацию
```

**Тесты и качество кода:**
```bash
make test             # Запуск тестов (без integration)
make test-cov         # Тесты с coverage
make format           # Форматирование кода
make lint             # Проверка качества кода
make check-all        # Полная проверка (format + lint + test-cov)
make clean            # Очистка логов
```

**Поздравляем! Вы прошли Getting Started 🎉**

