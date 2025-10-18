<!-- 6aa5541d-898c-441d-8e87-46157f17632b b4b8d8db-22fe-4ab4-aad9-c229927173a0 -->
# Sprint S1: Mock API для дашборда статистики

## Цель

Создать Mock API для получения статистики по сообщениям с возможностью последующей замены на реальную реализацию.

## Референс и метрики

- **Дизайн**: Shadcn UI dashboard-01 (https://ui.shadcn.com/blocks#dashboard-01)
- **Фокус**: Метрики сообщений (total, by role, over time, average length)

## Технологический стек

- **FastAPI** - современный async web framework с авто-документацией
- **Pydantic** - валидация данных и схемы API
- **Protocol pattern** - для абстракции Mock/Real реализаций

## Структура API

### Единый endpoint: `GET /api/v1/statistics`

**Query параметры:**

- `period` (optional) - период статистики: `day` | `week` | `month` | `all` (default: `month`)

**Примеры запросов:**

- `GET /api/v1/statistics` - статистика за месяц (default)
- `GET /api/v1/statistics?period=day` - статистика за день
- `GET /api/v1/statistics?period=week` - статистика за неделю
- `GET /api/v1/statistics?period=all` - вся статистика

Возвращает полную статистику для дашборда за указанный период:

```python
{
  "period": "month",  // Текущий выбранный период
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
    {"date": "2025-10-01", "count": 245},
    {"date": "2025-10-02", "count": 312},
    // Количество точек зависит от period:
    // day - 24 часа (по часам)
    // week - 7 дней
    // month - 30 дней
    // all - по месяцам за всё время
  ],
  "top_metrics": {
    "most_active_users": 5,
    "messages_today": 156,
    "messages_this_week": 1045,
    "messages_this_month": 4321
  }
}
```

## План реализации

### 1. Добавить зависимости

В `pyproject.toml`:

- `fastapi>=0.104`
- `uvicorn[standard]>=0.24` (ASGI server)
- `pydantic>=2.0`

### 2. Создать модели данных

Файл: `src/api/schemas.py`

- Pydantic модели для response (Overview, MessagesByRole, TimeSeries, Statistics)
- Type-safe структуры данных

### 3. Создать Protocol для StatCollector

Файл: `src/api/protocols.py`

```python
class StatCollectorProtocol(Protocol):
    async def get_statistics(self, period: str = "month") -> Statistics:
        """Get dashboard statistics for specified period.
        
        Args:
            period: Time period (day|week|month|all)
        """
        ...
```

### 4. Реализовать Mock StatCollector

Файл: `src/api/stat_collector_mock.py`

- Генерация реалистичных mock данных
- Случайные значения в разумных пределах
- Данные за последние 30 дней

### 5. Создать FastAPI приложение

Файл: `src/api/main.py`

- Router с endpoint `/api/v1/statistics`
- Dependency injection для StatCollector
- CORS middleware для frontend
- Auto-generated OpenAPI docs (встроено в FastAPI)

### 6. Добавить конфигурацию API

Расширить `src/config.py`:

- `API_HOST` (default: "0.0.0.0")
- `API_PORT` (default: 8000)
- `STAT_COLLECTOR_MODE` (default: "mock", options: "mock"|"real")

### 7. Создать entrypoint для API

Файл: `src/api_server.py`

- Загрузка конфигурации
- Инициализация StatCollector (Mock или Real)
- Запуск uvicorn server

### 8. Добавить Makefile команды

```makefile
api-run:          # Запуск API сервера (uvicorn)
api-test:         # Тест получения статистики (curl)
api-docs:         # Открыть Swagger UI
```

### 9. Написать тесты

Файл: `tests/test_api_mock.py`

- Тест Mock StatCollector
- Тест API endpoint с TestClient
- Проверка структуры response

### 10. Создать примеры запросов для тестирования

Файл: `doc/api-examples.md` или добавить в план

- Примеры curl команд для всех вариантов period
- Примеры ответов API
- Инструкции по ручному тестированию

### 11. Актуализировать roadmap

Файл: `frontend/doc/frontend-roadmap.md`

- Обновить статус спринта S1 на "✅ Completed"
- Добавить ссылку на план реализации в таблицу спринтов
- Указать дату завершения

## Файловая структура

```
src/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── protocols.py         # StatCollectorProtocol
│   ├── schemas.py           # Pydantic models
│   └── stat_collector_mock.py  # Mock implementation
├── api_server.py            # Entrypoint
└── config.py                # Updated with API settings

tests/
└── test_api_mock.py         # API tests
```

## Критерии успеха

- ✅ API возвращает корректную JSON структуру
- ✅ Swagger UI доступен по `/docs`
- ✅ Mock данные реалистичны и разнообразны
- ✅ Все тесты проходят
- ✅ Команды Makefile работают
- ✅ Готово к замене Mock → Real реализации

## Примечания

- Protocol pattern позволит легко переключиться с Mock на Real в Sprint S5
- FastAPI обеспечивает автоматическую документацию (Swagger/ReDoc)
- CORS настроен для работы с frontend разработкой
- Данные генерируются при каждом запросе (stateless Mock)

### To-dos

- [ ] Добавить FastAPI, Uvicorn, Pydantic в pyproject.toml
- [ ] Создать Pydantic модели для API response (schemas.py)
- [ ] Создать StatCollectorProtocol интерфейс
- [ ] Реализовать MockStatCollector с генерацией данных
- [ ] Создать FastAPI приложение с endpoint и CORS
- [ ] Расширить Config с настройками API
- [ ] Создать api_server.py entrypoint с uvicorn
- [ ] Добавить команды api-run, api-test, api-docs в Makefile
- [ ] Написать тесты для Mock API
- [ ] Создать примеры запросов к API для тестирования
- [ ] Обновить статус спринта S1 в frontend-roadmap.md на 'Completed'
- [ ] Добавить ссылку на план в таблицу спринтов в frontend-roadmap.md