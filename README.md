# systech-aidd-live

AI-powered Telegram chatbot с управлением контекстом диалога.

## Возможности

- Интеграция с Telegram Bot API через aiogram
- Работа с LLM через OpenAI Compatible API (OpenRouter)
- Управление контекстом диалога (in-memory)
- Команды: /start, /help, /reset
- Логирование всех операций

## Технологии

- Python 3.11+
- aiogram 3.x - асинхронная библиотека для Telegram Bot API
- openai - Python SDK для работы с LLM
- python-dotenv - загрузка переменных окружения
- uv - современный менеджер пакетов

## Быстрый старт

### 1. Установка зависимостей

```bash
make install
```

Или напрямую через uv:
```bash
uv sync
```

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

### 3. Запуск

```bash
make run
```

Или напрямую:
```bash
uv run python -m src.main
```

### 4. Остановка

Нажмите `Ctrl+C` в терминале.

## Команды

- `make install` - установка зависимостей
- `make run` - запуск бота
- `make test` - запуск тестов
- `make clean` - очистка логов

## Команды бота

- `/start` - начать работу с ботом
- `/help` - показать справку
- `/reset` - очистить историю диалога

## Структура проекта

```
systech-aidd-live/
├── src/                    # Исходный код
│   ├── __init__.py
│   ├── main.py            # Точка входа
│   ├── config.py          # Конфигурация
│   ├── message.py         # Класс Message
│   ├── message_handler.py # Обработка сообщений
│   ├── llm_client.py      # Работа с LLM API
│   └── context_manager.py # Управление контекстом
├── tests/                 # Тесты
├── logs/                  # Логи
├── doc/                   # Документация
├── .env                   # Конфигурация (не в git)
├── .env.example           # Пример конфигурации
├── pyproject.toml         # Зависимости
├── Makefile               # Команды автоматизации
└── README.md
```

## Особенности

- **KISS-принцип** - никакого оверинжиниринга
- **Один класс = один файл** - строгое правило
- **Асинхронный код** - async/await везде
- **Плоская структура** - все в src/ без вложенности
- **In-memory хранение** - без БД на этапе MVP

## Логи

Логи сохраняются в `logs/app.log` и выводятся в консоль.

## Лицензия

MIT


