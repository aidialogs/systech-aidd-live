<!-- 1c94bc81-7e5d-43fb-8541-bfa8f14d13dc 56927d3e-01b2-4661-b82b-609652c05a16 -->
# Итерация 2: Реализация Stats API с mock данными

## Цель

Создать REST API endpoint `/api/stats` с hardcoded mock данными для разработки frontend дашборда.

## 1. Зависимости (pyproject.toml)

Добавить в секцию `dependencies`:

```python
"fastapi>=0.104.0",
"uvicorn[standard]>=0.24.0",
```

Затем выполнить: `uv sync`

## 2. Protocol для StatsCollector (src/protocols.py)

Добавить в существующий файл:

```python
from typing import Any

class StatsCollectorProtocol(Protocol):
    """Protocol for stats collector implementations."""
    
    async def collect_stats(self, time_range: str = "7d") -> dict[str, Any]:
        """Collect statistics for the given time range."""
        ...
```

## 3. Mock реализация (src/mock_stats_collector.py)

Создать новый файл с hardcoded данными:

```python
from datetime import datetime, timedelta, timezone
from typing import Any

class MockStatsCollector:
    """Mock implementation with hardcoded demo data."""
    
    async def collect_stats(self, time_range: str = "7d") -> dict[str, Any]:
        """Return mock statistics with beautiful demo data."""
        
        # Overview metrics (hardcoded)
        overview = {
            "total_users": {
                "value": 150,
                "trend": 12.5,
                "trend_direction": "up"
            },
            "total_conversations": {
                "value": 234,
                "trend": -5.2,
                "trend_direction": "down"
            },
            "total_messages": {
                "value": 3420,
                "trend": 8.3,
                "trend_direction": "up"
            },
            "avg_conversation_length": {
                "value": 14.6,
                "trend": 2.1,
                "trend_direction": "up"
            }
        }
        
        # Message activity data points (generated based on time_range)
        days = 7 if time_range == "7d" else 30
        now = datetime.now(timezone.utc)
        
        # Hardcoded message counts for variety
        message_counts = [45, 52, 38, 61, 49, 55, 43]  # для 7d
        if days == 30:
            message_counts = [45, 52, 38, 61, 49, 55, 43, 50, 48, 56,
                            42, 58, 47, 53, 39, 62, 44, 57, 51, 46,
                            54, 41, 59, 48, 52, 43, 60, 49, 55, 47]
        
        data_points = []
        for i in range(days):
            timestamp = (now - timedelta(days=days-1-i)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            data_points.append({
                "timestamp": timestamp.isoformat(),
                "message_count": message_counts[i]
            })
        
        return {
            "overview": overview,
            "message_activity": {
                "time_range": time_range,
                "data_points": data_points
            }
        }
```

## 4. FastAPI приложение (src/api_server.py)

```python
import logging
import time
from typing import Any

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Stats API", version="0.1.0")

# CORS для localhost:3000 (Next.js dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing."""
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    logging.info(f"API request: {request.method} {request.url.path} - {duration:.0f}ms")
    return response

@app.get("/api/stats")
async def get_stats(
    request: Request,
    time_range: str = Query("7d", regex="^(7d|30d)$")
) -> dict[str, Any]:
    """Get bot statistics for the specified time range."""
    stats_collector = request.app.state.stats_collector
    stats = await stats_collector.collect_stats(time_range)
    logging.info(f"Stats collected: time_range={time_range}, "
                f"data_points={len(stats['message_activity']['data_points'])}")
    return stats

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "stats-api"}
```

## 5. Точка входа API (src/api_main.py)

```python
import asyncio
import logging
import os

import uvicorn
from dotenv import load_dotenv

from src.api_server import app
from src.config import Config
from src.mock_stats_collector import MockStatsCollector

async def main() -> None:
    """Main entry point for the API server."""
    load_dotenv()
    config = Config.from_env()
    
    # Setup logging (same as bot)
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
    )
    
    # Create mock stats collector
    stats_collector = MockStatsCollector()
    
    # Attach to app state
    app.state.stats_collector = stats_collector
    
    logging.info(f"API server starting on {config.api_host}:{config.api_port}")
    
    # Run uvicorn
    config_uvicorn = uvicorn.Config(
        app,
        host=config.api_host,
        port=config.api_port,
        log_level="info"
    )
    server = uvicorn.Server(config_uvicorn)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
```

## 6. Обновить Config (src/config.py)

Добавить поля в dataclass:

```python
api_host: str
api_port: int
```

В метод `from_env()` после max_context_messages добавить:

```python
# API server configuration
api_host = os.getenv("API_HOST", "0.0.0.0")
api_port = int(os.getenv("API_PORT", "8000"))
```

И в return добавить:

```python
api_host=api_host,
api_port=api_port,
```

## 7. Обновить .env.example

Добавить в конец файла (или создать файл если его нет):

```env
# API Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

## 8. Обновить Makefile

Добавить новые команды после `run`:

```makefile
run-api:
	uv run python -m src.api_main

api-check:
	@echo "🔍 Checking API endpoints..."
	@echo ""
	@echo "1. Health check:"
	@curl -s http://localhost:8000/health | python -m json.tool
	@echo ""
	@echo "2. Stats (default 7d):"
	@curl -s http://localhost:8000/api/stats | python -m json.tool
	@echo ""
	@echo "3. Stats (30d):"
	@curl -s "http://localhost:8000/api/stats?time_range=30d" | python -m json.tool
	@echo ""
	@echo "✅ API check complete. Open http://localhost:8000/docs for Swagger UI"
```

## Итоговая структура файлов

```
src/
├── protocols.py           # +StatsCollectorProtocol
├── mock_stats_collector.py  # НОВЫЙ: hardcoded mock данные
├── api_server.py          # НОВЫЙ: FastAPI app
├── api_main.py            # НОВЫЙ: точка входа API
├── config.py              # +api_host, api_port
└── ... (остальные файлы)
```

## Ключевые решения

1. **Protocol + Mock** - StatsCollectorProtocol интерфейс, MockStatsCollector с hardcoded данными
2. **Один класс = один файл** - MockStatsCollector в отдельном файле
3. **Hardcoded mock данные** - красивые числа прямо в коде для демонстрации
4. **Query параметр time_range** - поддержка 7d и 30d с валидацией через regex
5. **CORS** - разрешен только для localhost:3000
6. **Async everywhere** - все методы async
7. **DI через app.state** - stats_collector передается через FastAPI state
8. **Без тестов** - MVP без тестов API (можно добавить позже)
9. **make api-check** - удобная команда для проверки всех endpoints с форматированным JSON

## Мануальное тестирование

1. Установить зависимости: `uv sync`
2. Запустить API: `make run-api`
3. В другом терминале запустить проверку: `make api-check`
4. Альтернативно проверить вручную:

   - Health: `curl http://localhost:8000/health`
   - Stats 7d: `curl http://localhost:8000/api/stats`
   - Stats 30d: `curl "http://localhost:8000/api/stats?time_range=30d"`

5. Открыть Swagger UI: `http://localhost:8000/docs`
6. Проверить логи: `tail -f logs/app.log`