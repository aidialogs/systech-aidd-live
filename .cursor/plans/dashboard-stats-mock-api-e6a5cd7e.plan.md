<!-- e6a5cd7e-f1be-4307-a9cd-747fa8c725a0 2268e89d-81e4-4881-b627-268358c3ca3c -->
# Итерация 1: Анализ требований и Stats API (Mock)

## Цель

Сформировать требования к дашборду статистики, спроектировать API контракт и реализовать Mock версию для разработки frontend

## Структура файлов

Создаваемые файлы:

- `frontend/doc/dashboard-requirements.md` - требования к UI дашборда
- `src/protocols.py` - добавить `StatsCollectorProtocol` и dataclasses
- `src/mock_stats_collector.py` - Mock реализация с генерацией данных
- `src/api/__init__.py` - пакет для API
- `src/api/server.py` - FastAPI приложение с `/api/stats` endpoint
- `src/api/main.py` - entry point для запуска API сервера (отдельно от бота)
- `tests/test_mock_stats_collector.py` - unit тесты Mock реализации

Обновляемые файлы:

- `pyproject.toml` - добавить fastapi, uvicorn в зависимости
- `Makefile` - добавить команды `api-run`, `api-dev`, `api-test`

## Детали реализации

### 1. Dashboard Requirements (`frontend/doc/dashboard-requirements.md`)

Документ с описанием:

- **4 карточки метрик** (адаптированные под структуру данных бота):
  - **Total Users**: общее количество пользователей с трендом
  - **Active Dialogs**: количество уникальных активных диалогов (user+chat) с трендом
  - **Total Messages**: общее количество сообщений с трендом
  - **Avg Message Length**: средняя длина сообщения (в символах) с трендом
- **График Messages Over Time**: временной ряд сообщений с переключателями периода
  - **Переключатели**: Last 7 days / Last 30 days
  - Данные адаптируются в зависимости от выбранного периода
- **Референс**: ссылка на shadcn/ui dashboard-01 и front-reference.png
- **UI компоненты**: структура layout на основе референса

### 2. StatsCollectorProtocol (`src/protocols.py`)

Добавить Protocol интерфейс и dataclasses:

```python
from dataclasses import dataclass
from typing import Protocol

@dataclass
class MetricCard:
    """Метрика для карточки дашборда."""
    title: str
    value: str
    trend: str  # "+12.5%", "-20%", "+4.5%"
    description: str

@dataclass
class ChartDataPoint:
    """Точка данных для графика."""
    date: str  # ISO 8601 UTC format: "2025-01-05T00:00:00Z"
    value: int

@dataclass
class DashboardStats:
    """Полная статистика для дашборда."""
    total_users: MetricCard
    active_dialogs: MetricCard
    total_messages: MetricCard
    avg_message_length: MetricCard
    messages_chart_7d: list[ChartDataPoint]  # 7 точек
    messages_chart_30d: list[ChartDataPoint]  # 30 точек

class StatsCollectorProtocol(Protocol):
    """Protocol для сбора статистики."""
    
    async def get_dashboard_stats(self) -> DashboardStats:
        """Получить статистику для дашборда."""
        ...
```

### 3. MockStatsCollector (`src/mock_stats_collector.py`)

Класс с генерацией правдоподобных данных:

- Использовать `random` для генерации значений
- Реалистичные тренды (+/-процент)
- График 7d: 7 точек (последние 7 дней)
- График 30d: 30 точек (последние 30 дней)
- Волнообразный паттерн для графика (имитация активности)

### 4. FastAPI Server (`src/api/server.py`)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.mock_stats_collector import MockStatsCollector

app = FastAPI(title="AIDD Stats API", version="1.0.0")

# CORS для локальной разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/stats")
async def get_stats():
    """Получить статистику дашборда."""
    collector = MockStatsCollector()
    stats = await collector.get_dashboard_stats()
    return stats
```

### 5. API Main (`src/api/main.py`)

Entry point для запуска API сервера (отдельно от бота):

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=8000, reload=True)
```

### 6. Зависимости (`pyproject.toml`)

Добавить в dependencies:

```toml
dependencies = [
    ...existing...,
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
]
```

### 7. Makefile команды

```makefile
# API сервер (отдельно от бота)
api-run:
    uv run python -m src.api.main

api-dev:
    uv run uvicorn src.api.server:app --reload --port 8000

api-test:
    curl -s http://localhost:8000/api/stats | python -m json.tool
```

### 8. Тестирование (`tests/test_mock_stats_collector.py`)

Unit тесты:

- Проверка структуры DashboardStats
- Проверка диапазонов значений
- Проверка формата тренда (regex: `^[+-]\d+(\.\d+)?%$`)
- Проверка длины графика (7d: 7 точек, 30d: 30 точек)
- Проверка что значения в разумных пределах

## Пример JSON ответа API

```json
{
  "total_users": {
    "title": "Total Users",
    "value": "1,234",
    "trend": "+12.5%",
    "description": "Total registered users"
  },
  "active_dialogs": {
    "title": "Active Dialogs",
    "value": "456",
    "trend": "+8.3%",
    "description": "Unique active conversations"
  },
  "total_messages": {
    "title": "Total Messages",
    "value": "45,678",
    "trend": "+15.2%",
    "description": "All messages exchanged"
  },
  "avg_message_length": {
    "title": "Avg Message Length",
    "value": "127",
    "trend": "-2.1%",
    "description": "Average characters per message"
  },
  "messages_chart_7d": [
    {"date": "Jan 10", "value": 1234},
    {"date": "Jan 11", "value": 1456},
    {"date": "Jan 12", "value": 1389},
    {"date": "Jan 13", "value": 1567},
    {"date": "Jan 14", "value": 1423},
    {"date": "Jan 15", "value": 1678},
    {"date": "Jan 16", "value": 1789}
  ],
  "messages_chart_30d": [
    {"date": "Dec 18", "value": 1100},
    {"date": "Dec 19", "value": 1150},
    ...
    {"date": "Jan 16", "value": 1789}
  ]
}
```

## Критерии готовности

- [x] `dashboard-requirements.md` создан с описанием всех компонентов UI
- [x] `StatsCollectorProtocol` добавлен в `src/protocols.py` с type hints
- [x] `MockStatsCollector` реализован и генерирует данные
- [x] FastAPI endpoint `/api/stats` работает и отдает JSON
- [x] CORS настроен для `localhost:3000`
- [x] Unit тесты покрывают Mock реализацию (100%)
- [x] Makefile команды `api-run`, `api-dev`, `api-test` работают
- [x] API документация доступна на `/docs` (автоматически через FastAPI)

## Тестирование

Запустить API сервер (отдельный процесс, не бот):

```bash
make api-dev
```

Проверить endpoint:

```bash
make api-test
```

Или напрямую:

```bash
curl http://localhost:8000/api/stats
```

Открыть Swagger UI:

```
http://localhost:8000/docs
```

Проверить что:

1. JSON возвращается в правильной структуре (4 метрики + 2 графика)
2. Все метрики присутствуют с трендами
3. График 7d содержит 7 точек, 30d - 30 точек
4. CORS headers присутствуют (для frontend запросов)
5. Значения реалистичные и в разумных пределах

### To-dos

- [ ] Создать frontend/doc/dashboard-requirements.md с описанием метрик и UI компонентов
- [ ] Добавить StatsCollectorProtocol, MetricCard, ChartDataPoint, DashboardStats в src/protocols.py
- [ ] Реализовать MockStatsCollector в src/mock_stats_collector.py с генерацией данных
- [ ] Создать src/api/ пакет с __init__.py, server.py (FastAPI app + CORS), main.py (uvicorn)
- [ ] Реализовать GET /api/stats endpoint в src/api/server.py
- [ ] Добавить fastapi>=0.109.0, uvicorn[standard]>=0.27.0 в pyproject.toml
- [ ] Добавить команды api-run и api-dev в Makefile
- [ ] Создать tests/test_mock_stats_collector.py с unit тестами (100% coverage)