# API Examples

Примеры запросов к Statistics Dashboard API.

## Запуск API сервера

```bash
# Установить зависимости
make install

# Запустить API сервер
make api-run

# Или напрямую через uv
uv run python -m src.api_server
```

API будет доступен по адресу: `http://localhost:8000`

## Health Check

Проверка работоспособности API:

```bash
curl http://localhost:8000/health
```

**Ответ:**
```json
{
  "status": "ok"
}
```

## Получение статистики

### Статистика за месяц (по умолчанию)

```bash
curl http://localhost:8000/api/v1/statistics
```

**Ответ:**
```json
{
  "period": "month",
  "overview": {
    "total_messages": 15234,
    "total_users": 342,
    "active_chats": 256,
    "avg_message_length": 87
  },
  "messages_by_role": {
    "user": 8456,
    "assistant": 6234,
    "system": 544
  },
  "messages_over_time": [
    {"date": "2025-09-18", "count": 245},
    {"date": "2025-09-19", "count": 312},
    ...
    {"date": "2025-10-17", "count": 423}
  ],
  "top_metrics": {
    "most_active_users": 5,
    "messages_today": 156,
    "messages_this_week": 1045,
    "messages_this_month": 4321
  }
}
```

### Статистика за день

Возвращает почасовую статистику за последние 24 часа:

```bash
curl "http://localhost:8000/api/v1/statistics?period=day"
```

**Ответ содержит 24 точки данных** (по одной на каждый час):
```json
{
  "period": "day",
  "overview": {...},
  "messages_by_role": {...},
  "messages_over_time": [
    {"date": "2025-10-16 18:00", "count": 45},
    {"date": "2025-10-16 19:00", "count": 52},
    ...
    {"date": "2025-10-17 17:00", "count": 68}
  ],
  "top_metrics": {...}
}
```

### Статистика за неделю

Возвращает дневную статистику за последние 7 дней:

```bash
curl "http://localhost:8000/api/v1/statistics?period=week"
```

**Ответ содержит 7 точек данных** (по одной на каждый день):
```json
{
  "period": "week",
  "overview": {...},
  "messages_by_role": {...},
  "messages_over_time": [
    {"date": "2025-10-11", "count": 145},
    {"date": "2025-10-12", "count": 212},
    ...
    {"date": "2025-10-17", "count": 189}
  ],
  "top_metrics": {...}
}
```

### Вся статистика

Возвращает месячную статистику за последние 12 месяцев:

```bash
curl "http://localhost:8000/api/v1/statistics?period=all"
```

**Ответ содержит 12 точек данных** (по одной на каждый месяц):
```json
{
  "period": "all",
  "overview": {...},
  "messages_by_role": {...},
  "messages_over_time": [
    {"date": "2024-11", "count": 1245},
    {"date": "2024-12", "count": 2012},
    ...
    {"date": "2025-10", "count": 2189}
  ],
  "top_metrics": {...}
}
```

## Автоматическое тестирование

Используйте готовую команду Makefile для быстрого тестирования всех endpoints:

```bash
make api-test
```

Эта команда выполнит:
1. Health check
2. Статистику с периодом по умолчанию (month)
3. Статистику за день (period=day)

## Swagger UI документация

Интерактивная документация API доступна по адресу:

```bash
# Открыть в браузере
make api-docs

# Или вручную
open http://localhost:8000/docs
```

В Swagger UI вы можете:
- Просмотреть все доступные endpoints
- Протестировать API прямо в браузере
- Посмотреть структуру request/response
- Скачать OpenAPI спецификацию

## ReDoc документация

Альтернативная документация в формате ReDoc:

```
http://localhost:8000/redoc
```

## OpenAPI спецификация

JSON спецификация API:

```bash
curl http://localhost:8000/openapi.json
```

## Использование из Python

```python
import httpx
import asyncio

async def get_statistics(period: str = "month"):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/v1/statistics",
            params={"period": period}
        )
        return response.json()

# Запуск
stats = asyncio.run(get_statistics("week"))
print(f"Total messages: {stats['overview']['total_messages']}")
```

## Использование из JavaScript

```javascript
// Fetch API
async function getStatistics(period = "month") {
  const response = await fetch(
    `http://localhost:8000/api/v1/statistics?period=${period}`
  );
  return await response.json();
}

// Использование
getStatistics("week").then(stats => {
  console.log(`Total messages: ${stats.overview.total_messages}`);
});
```

## Обработка ошибок

### Невалидный период

```bash
curl "http://localhost:8000/api/v1/statistics?period=invalid"
```

**Ответ (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "string_pattern_mismatch",
      "loc": ["query", "period"],
      "msg": "String should match pattern '^(day|week|month|all)$'",
      "input": "invalid"
    }
  ]
}
```

## Конфигурация

API настраивается через переменные окружения в `.env`:

```bash
# API settings
API_HOST=0.0.0.0
API_PORT=8000
STAT_COLLECTOR_MODE=mock  # mock или real (real будет в Sprint S5)
```

## CORS

API настроен с разрешением CORS для всех источников в режиме разработки.

Для production окружения нужно будет указать конкретные разрешенные домены в `src/api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

