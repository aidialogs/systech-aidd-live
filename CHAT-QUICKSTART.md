# AI Chat - Quick Start Guide

## Запуск системы

### 1. Настройка окружения

Убедитесь что `.env` содержит:
```bash
# LLM Configuration
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname

# API Configuration
STAT_COLLECTOR_MODE=real  # Используем реальную БД
```

### 2. Запуск Backend API

```bash
# Из корня проекта
make api-run
```

API будет доступен на `http://localhost:8000`

### 3. Запуск Frontend

```bash
# В отдельном терминале
make frontend-dev
```

Frontend будет доступен на `http://localhost:3000`

### 4. Или запустите все сразу

```bash
make dev
```

## Использование чата

### Вариант 1: Floating Button

1. Откройте `http://localhost:3000` или `http://localhost:3000/dashboard`
2. В правом нижнем углу появится круглая кнопка с иконкой бота
3. Нажмите на кнопку - откроется чат overlay
4. Выберите режим: **Normal** или **Admin**
5. Начните общение!

### Вариант 2: Полноэкранный чат

1. Откройте `http://localhost:3000/chat`
2. Выберите режим в header
3. Начните общение!

## Режимы работы

### 🤖 Normal Mode

**Для чего**: Обычное общение с AI ассистентом

**Примеры вопросов**:
- "Объясни что такое Docker"
- "Как работает async/await в Python?"
- "Напиши функцию для сортировки массива"
- "Что такое REST API?"

**Особенности**:
- Используется system prompt из конфигурации
- История сохраняется в БД
- Контекст поддерживается автоматически
- Работает как Telegram бот

### 📊 Admin Mode

**Для чего**: Аналитика данных через natural language queries

**Примеры вопросов**:
- "Сколько всего сообщений в базе данных?"
- "Покажи топ-5 самых активных пользователей"
- "Сколько сообщений было отправлено сегодня?"
- "Какое среднее количество сообщений у пользователей?"
- "Покажи количество сообщений по ролям"

**Особенности**:
- Автоматическая генерация SQL из вопроса
- Выполнение запроса к реальной БД
- Отображение SQL запроса (для отладки)
- Понятный ответ от LLM на основе данных
- Только SELECT запросы (безопасность)

## Тестирование через curl

### Normal Mode

```bash
make chat-test

# Или напрямую:
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "mode": "normal",
    "user_id": 1,
    "chat_id": 1
  }' | python3 -m json.tool
```

### Admin Mode

```bash
make chat-test-admin

# Или напрямую:
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Сколько всего сообщений?",
    "mode": "admin",
    "user_id": 1,
    "chat_id": 1
  }' | python3 -m json.tool
```

### История чата

```bash
make chat-history

# Или напрямую:
curl http://localhost:8000/api/v1/chat/history?user_id=1&chat_id=1&limit=10 \
  | python3 -m json.tool
```

## Dashboard с реальными данными

Дашборд теперь показывает реальную статистику из БД:

```bash
# Откройте
http://localhost:3000/dashboard

# Все метрики берутся из PostgreSQL:
- Общее количество сообщений
- Количество пользователей
- Активные чаты
- Средняя длина сообщения
- Графики по времени
- Распределение по ролям
```

## Переключение Mock/Real режима

В `.env` измените:

```bash
# Для тестирования без БД
STAT_COLLECTOR_MODE=mock

# Для работы с реальной БД
STAT_COLLECTOR_MODE=real
```

После изменения перезапустите API.

## API Documentation

Swagger UI доступен на:
```
http://localhost:8000/docs
```

ReDoc доступен на:
```
http://localhost:8000/redoc
```

## Troubleshooting

### Чат не отвечает

1. Проверьте что API запущен: `curl http://localhost:8000/health`
2. Проверьте LLM_API_KEY в `.env`
3. Проверьте логи API сервера

### Нет истории сообщений

1. Убедитесь что БД доступна
2. Проверьте DATABASE_URL в `.env`
3. Запустите миграции: `make db-migrate`

### Admin mode не работает

1. Проверьте что STAT_COLLECTOR_MODE=real
2. Убедитесь что таблицы users и messages существуют
3. Проверьте логи - там будет показан сгенерированный SQL

### Frontend ошибки

1. Проверьте что NEXT_PUBLIC_API_URL указывает на API
2. Очистите кэш: `cd frontend && pnpm clean`
3. Переустановите зависимости: `cd frontend && pnpm install`

## Примеры сложных запросов в Admin Mode

### Аналитика пользователей
```
"Покажи пользователей, которые отправили больше 10 сообщений"
```

### Временная аналитика
```
"Сколько сообщений было отправлено в последнюю неделю?"
```

### Агрегация
```
"Какая средняя длина сообщения у пользователей?"
```

### Группировка
```
"Покажи количество сообщений по дням за последний месяц"
```

## Архитектура

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Browser   │─────▶│  Next.js     │─────▶│  FastAPI    │
│  (Chat UI)  │◀─────│  (Frontend)  │◀─────│  (Backend)  │
└─────────────┘      └──────────────┘      └─────────────┘
                                                   │
                                                   ▼
                                            ┌─────────────┐
                                            │ PostgreSQL  │
                                            │     БД      │
                                            └─────────────┘
                                                   │
                                                   ▼
                                            ┌─────────────┐
                                            │  LLM API    │
                                            │ (OpenAI)    │
                                            └─────────────┘
```

## Дополнительно

### Логи

Backend логи в `logs/app.log`

Frontend логи в консоли браузера (F12)

### Мониторинг

Проверить health: `curl http://localhost:8000/health`

Swagger docs: `http://localhost:8000/docs`

### Разработка

Для изменения UI компонентов смотрите:
- `frontend/src/components/chat/` - чат компоненты
- `frontend/src/components/ui/` - базовые UI компоненты

Для изменения backend логики:
- `src/api/chat_handler.py` - обработка сообщений
- `src/api/stat_collector_real.py` - статистика из БД

---

**Готово!** Система работает и готова к использованию 🚀



