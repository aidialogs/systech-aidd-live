# GUIDE-01: Getting Started

**Цель**: За 15 минут запустить бота локально и отправить первое сообщение.

---

## Prerequisites

Перед началом убедитесь, что установлено:

- **Python 3.11+** — проверьте версию: `python --version`
- **uv** — современный менеджер пакетов Python

### Установка uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# или через pip
pip install uv
```

После установки перезапустите терминал и проверьте: `uv --version`

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
# Обязательные параметры
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
LLM_API_KEY=sk-or-v1-xxxxxxxxxxxxx
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet

# Опциональные (можно оставить как есть)
SYSTEM_PROMPT_FILE=prompts/system_prompt.txt
MAX_CONTEXT_MESSAGES=20
```

**Важно**: Файл `.env` НЕ должен попадать в git (уже в `.gitignore`).

---

## Шаг 5: Запуск бота

```bash
make run
```

Вы должны увидеть:

```
2025-10-16 14:23:45 | INFO | System prompt loaded from file: prompts/system_prompt.txt
2025-10-16 14:23:45 | INFO | Bot started
```

Бот работает! Оставьте терминал открытым.

---

## Шаг 6: Тестирование

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

## Шаг 7: Остановка бота

В терминале нажмите **Ctrl+C**

Вы увидите:
```
2025-10-16 14:25:30 | INFO | Bot stopped
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

---

## Troubleshooting

### ❌ "Command not found: uv"
```bash
# Переустановите uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# Перезапустите терминал
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

### ❌ Бот не отвечает в Telegram
1. Убедитесь, что бот запущен (терминал с `make run`)
2. Проверьте, что `BOT_TOKEN` правильный (нет лишних символов)
3. Попробуйте `/start` — если не отвечает, пересоздайте бота через @BotFather

---

## Что дальше?

✅ Бот запущен и работает!

Переходите к следующим гайдам:
- **GUIDE-02**: Архитектура проекта — как устроена система
- **GUIDE-06**: Codebase Tour — обзор всех файлов
- **GUIDE-07**: Development Workflow — как добавлять новые фичи
- **GUIDE-08**: Testing — как писать и запускать тесты

---

## Полезные команды

```bash
make run              # Запуск бота
make test             # Запуск тестов (без integration)
make test-cov         # Тесты с coverage
make format           # Форматирование кода
make lint             # Проверка качества кода
make check-all        # Полная проверка (format + lint + test-cov)
make clean            # Очистка логов
```

**Поздравляем! Вы прошли Getting Started 🎉**

