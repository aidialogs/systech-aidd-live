# 🚀 Getting Started Guide

**Цель**: Запустить проект за 15 минут  
**Для кого**: Новый разработчик, первый день

---

## 📋 Prerequisites Checklist

Перед началом работы убедитесь что у вас установлено:

- ✅ **Python 3.11+** - `python --version`
- ✅ **uv** - современный менеджер пакетов Python
- ✅ **Git** - для клонирования репозитория
- ✅ **Telegram аккаунт** - для тестирования бота
- ✅ **Telegram Bot Token** - получить через [@BotFather](https://t.me/BotFather)
- ✅ **LLM API Key** - получить на [OpenRouter](https://openrouter.ai/)

---

## 🔧 Шаг 1: Установка uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# или через pip
pip install uv

# Проверка установки
uv --version
```

---

## 📥 Шаг 2: Клонирование и установка

```bash
# Клонировать репозиторий
git clone <repository-url>
cd systech-aidd-live

# Установить зависимости (создаст .venv/)
make install

# Альтернатива
uv sync --extra dev
```

**Что происходит**:
- Создается виртуальное окружение `.venv/`
- Устанавливаются зависимости из `pyproject.toml`
- Загружается lock-файл `uv.lock` для воспроизводимости

---

## ⚙️ Шаг 3: Конфигурация

### 3.1 Создать файл .env

```bash
cp .env.example .env
```

### 3.2 Получить Telegram Bot Token

1. Открыть [@BotFather](https://t.me/BotFather) в Telegram
2. Отправить команду `/newbot`
3. Следовать инструкциям (имя бота, username)
4. Скопировать токен вида `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### 3.3 Получить LLM API Key

1. Зарегистрироваться на [OpenRouter.ai](https://openrouter.ai/)
2. Пополнить баланс ($5-10 для начала)
3. Создать API Key в настройках
4. Скопировать ключ вида `sk-or-v1-xxxxxxxxxxxxx`

### 3.4 Заполнить .env

```bash
# Обязательные параметры
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
LLM_API_KEY=sk-or-v1-xxxxxxxxxxxxx
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet

# Опциональные (можно оставить по умолчанию)
SYSTEM_PROMPT_FILE=prompts/system_prompt.txt
MAX_CONTEXT_MESSAGES=20
```

**Важно**: Никогда не коммитить `.env` в git!

---

## 🎯 Шаг 4: Запуск бота

```bash
make run

# Альтернатива
uv run python -m src.main
```

**Ожидаемый вывод**:
```
2025-10-15 10:00:00 | INFO | Bot started
2025-10-15 10:00:01 | INFO | Polling started
```

**Если видите ошибки** → см. [Troubleshooting](12-troubleshooting.md)

---

## ✅ Шаг 5: Smoke Test

### 5.1 Найти бота в Telegram

Откройте Telegram и найдите бота по username, который вы указали при создании.

### 5.2 Протестировать команды

```
/start
→ Бот должен ответить приветствием

/help
→ Бот должен показать список команд

Привет, как дела?
→ Бот должен ответить через LLM

/reset
→ История диалога очищена
```

### 5.3 Проверить логи

```bash
# Логи должны появиться в logs/app.log
cat logs/app.log

# Или следить за логами в реальном времени
tail -f logs/app.log
```

---

## 🧪 Шаг 6: Запуск тестов

```bash
# Запустить unit тесты (быстро, ~2-3 секунды)
make test

# Запустить тесты с coverage
make test-cov

# Запустить все тесты включая integration
make test-all
```

**Ожидаемый результат**:
```
====== 29 passed in 2.8s ======
Coverage: 100%
```

---

## 🎉 Готово!

Если все шаги выше прошли успешно:

✅ Бот запущен и работает  
✅ Команды отвечают корректно  
✅ LLM интеграция работает  
✅ Тесты проходят  
✅ Логи пишутся  

**Следующие шаги**:

1. [Repository Tour](02-repository-tour.md) - изучить структуру проекта
2. [Architecture Overview](03-architecture-overview.md) - понять как работает система
3. [Development Workflow](06-development-workflow.md) - начать разработку

---

## ⏱️ Время выполнения

- **Установка prereqs**: 5 минут
- **Клонирование и setup**: 3 минуты
- **Конфигурация**: 5 минут
- **Запуск и тестирование**: 2 минуты

**Total**: ~15 минут ⚡

---

## 🆘 Если что-то не работает

См. [Troubleshooting Guide](12-troubleshooting.md) для решения типичных проблем:

- ❌ Command not found: uv
- ❌ Invalid BOT_TOKEN
- ❌ LLM API errors
- ❌ Tests failing
- ❌ Import errors

---

## 📚 Дополнительные ресурсы

- [README.md](../../README.md) - полная документация
- [QUICKSTART.md](../../QUICKSTART.md) - краткий quickstart
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [OpenRouter Documentation](https://openrouter.ai/docs)

