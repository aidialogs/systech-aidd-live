<!-- e37197b4-4a19-4430-8478-970fcf56d365 a97b0fdb-a465-4c7d-b082-770e39ca39e9 -->
# План спринта F1: Требования к дашборду и Mock API

## Обзор

Создать документацию требований к дашборду статистики, спроектировать API контракт и реализовать Mock API сервер на FastAPI с автогенерацией документации.

## Структура создаваемых файлов

```
frontend/doc/dashboard-requirements.md     # Функциональные требования
src/api/__init__.py                        # API пакет
src/api/main.py                           # FastAPI приложение
src/api/server.py                         # Entrypoint для запуска API
src/mock_stats_collector.py              # Mock реализация сборщика статистики
src/protocols.py                          # Добавить StatCollectorProtocol
```

## Задачи реализации

### 1. Документ функциональных требований

**Файл:** `frontend/doc/dashboard-requirements.md`

Создать документ с описанием:

- **4 метрики-карточки** (по референсу):
  - Количество пользователей (всего) + тренд за 30 дней
  - Количество диалогов (chat_id) + тренд за 30 дней  
  - Количество сообщений (всего) + тренд за 30 дней
  - Средняя длина сообщений + тренд за 30 дней

- **График Timeline**:
  - Количество сообщений по дням
  - Фильтры: "Last 7 days", "Last 30 days"
  - Отображение с группировкой по дням

- **Требования к отображению**:
  - Тренды: иконка ↑/↓, процент изменения, цвет (зеленый/красный)
  - Формат чисел с разделителями тысяч
  - Темная тема (по референсу)

### 2. StatCollectorProtocol интерфейс

**Файл:** `src/protocols.py`

Добавить Protocol для сборщика статистики:

```python
class StatCollectorProtocol(Protocol):
    """Protocol for statistics collection."""
    
    async def get_stats(self, period_days: int) -> dict[str, Any]:
        """Get statistics for specified period."""
        ...
```

### 4. Mock реализация StatCollector

**Файл:** `src/mock_stats_collector.py`

Создать класс `MockStatCollector` с фиксированными данными:

```python
class MockStatCollector:
    """Mock implementation of statistics collector with fixed data."""
    
    async def get_stats(self, period_days: int) -> dict[str, Any]:
        """Return fixed mock statistics data."""
        # Фиксированные данные для метрик и timeline
        # Разные наборы для period_days=7 и period_days=30
        ...
```

**Данные:**

- Для 7 дней: 7 точек на графике
- Для 30 дней: 30 точек на графике  
- Метрики с трендами (% изменения)
- Без random генерации - только фиксированные значения

### 5. FastAPI приложение

**Файл:** `src/api/main.py`

Создать FastAPI приложение:

```python
from fastapi import FastAPI, Query
from src.mock_stats_collector import MockStatCollector
from enum import Enum

class Period(str, Enum):
    SEVEN_DAYS = "7d"
    THIRTY_DAYS = "30d"

app = FastAPI(
    title="Systech AIDD Stats API",
    description="API для получения статистики по диалогам",
    version="1.0.0"
)

stats_collector = MockStatCollector()

@app.get("/api/stats")
async def get_stats(period: Period = Query(Period.SEVEN_DAYS)):
    """Получить статистику за указанный период."""
    period_days = 7 if period == Period.SEVEN_DAYS else 30
    return await stats_collector.get_stats(period_days)

@app.get("/")
async def root():
    return {"message": "Systech AIDD Stats API", "docs": "/docs"}
```

**Особенности:**

- Автогенерация OpenAPI документации (доступна на `/docs`)
- CORS middleware для frontend (allow all origins для dev)
- Без аутентификации
- Порт 8000

### 6. Entrypoint для запуска API

**Файл:** `src/api/server.py`

Создать скрипт запуска:

```python
"""API server entrypoint."""
import uvicorn

def main() -> None:
    """Run API server."""
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
```

### 7. Обновление зависимостей

**Файл:** `pyproject.toml`

Добавить FastAPI зависимости:

```toml
dependencies = [
    # ... existing
    "fastapi>=0.104",
    "uvicorn[standard]>=0.24",
]
```

### 8. Команды в Makefile

**Файл:** `Makefile`

Добавить команды:

```makefile
# API Server
api-run:
	uv run python -m src.api.server

api-docs:
	@echo "API Documentation: http://localhost:8000/docs"
	@echo "API Stats endpoint: http://localhost:8000/api/stats?period=7d"

api-test:
	curl -s http://localhost:8000/api/stats?period=7d | python -m json.tool
```

## Проверка результата

1. Запустить API: `make api-run`
2. Открыть документацию: http://localhost:8000/docs
3. Протестировать endpoint: `make api-test`
4. Проверить оба периода: 7d и 30d
5. Убедиться что данные фиксированные и структура соответствует контракту

### To-dos

- [ ] Создать frontend/doc/dashboard-requirements.md с функциональными требованиями к дашбордуСоздать frontend/doc/api-contract.md с описанием REST API контракта
- [ ] Добавить StatCollectorProtocol в src/protocols.py
- [ ] Создать src/mock_stats_collector.py с MockStatCollector и фиксированными данными
- [ ] Создать src/api/__init__.py и src/api/main.py с FastAPI приложением
- [ ] Создать src/api/server.py - entrypoint для запуска API сервера
- [ ] Добавить fastapi и uvicorn в pyproject.toml и выполнить uv sync
- [ ] Добавить команды api-run, api-docs, api-test в Makefile
- [ ] Протестировать API: запуск, документация, получение статистики для обоих периодов