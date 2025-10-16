# ADR-06: Персистентное хранение данных (PostgreSQL + psycopg3 + Yoyo)

**Статус:** Принято  
**Дата:** 2025-10-15  
**Контекст:** Спринт S1 - Persistent Storage

---

## Контекст

После завершения спринта S0 (MVP + Tech Debt Elimination) бот работает с in-memory хранилищем контекста диалогов. Это означает:
- История диалогов теряется при перезапуске бота
- Невозможность масштабирования на несколько инстансов
- Отсутствие персистентности данных

**Требования:**
- Сохранение истории диалогов между перезапусками
- Простое решение (принцип KISS)
- Асинхронность (совместимость с aiogram)
- Минимальные изменения в существующей архитектуре

## Решение

### 1. Выбор СУБД: PostgreSQL

**Альтернативы:**
- SQLite - простой, но проблемы с конкурентностью
- MongoDB - избыточно для нашей задачи
- PostgreSQL - надежный, поддержка async, хорошо знакомый

**Решение:** PostgreSQL через Docker для локальной разработки

**Преимущества:**
- ✅ Production-ready решение
- ✅ Отличная поддержка транзакций
- ✅ Богатые типы данных
- ✅ Хорошая документация

### 2. Выбор драйвера: psycopg3

**Альтернативы:**
- `psycopg2` - популярный, но синхронный (не подходит для aiogram)
- `asyncpg` - самый быстрый, но специфичный API (не DB-API 2.0)
- `psycopg3` - современный, асинхронный, стандартный API

**Решение:** `psycopg[binary]>=3.0`

**Преимущества:**
- ✅ Полная асинхронная поддержка
- ✅ Совместимость с aiogram
- ✅ DB-API 2.0 standard
- ✅ Активная разработка

### 3. Уровень абстракции: Прямой SQL

**Альтернативы:**
- SQLAlchemy ORM - избыточно, много "магии"
- SQLAlchemy Core - SQL builder, средний уровень абстракции
- Прямой SQL - максимальная простота и контроль

**Решение:** Прямые SQL запросы через psycopg3

**Преимущества:**
- ✅ Максимальная простота (KISS)
- ✅ Полный контроль над запросами
- ✅ Легко понять что происходит
- ✅ Минимум зависимостей

### 4. Миграции: Yoyo

**Альтернативы:**
- Flyway - требует Java runtime
- Alembic - интеграция с SQLAlchemy, автогенерация (не нужна без ORM)
- Yoyo - простой, SQL-based, Python-native

**Решение:** `yoyo-migrations>=8.0`

**Преимущества:**
- ✅ Простые SQL файлы
- ✅ Python-native (без Java)
- ✅ Минимум абстракций
- ✅ Версионирование схемы БД

## Архитектурные изменения

### 1. Схема базы данных

Одна простая таблица `messages`:

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_chat ON messages(user_id, chat_id);
CREATE INDEX idx_created_at ON messages(created_at);
```

**Обоснование:**
- Простая нормализованная структура
- Индексы для быстрого поиска по `(user_id, chat_id)`
- Минимум колонок - только необходимое

### 2. Новый модуль: `src/database.py`

**DatabaseRepository:**
```python
class DatabaseRepository:
    def __init__(self, pool: AsyncConnectionPool) -> None:
        self.pool = pool
    
    async def save_message(user_id, chat_id, role, content) -> None
    async def get_messages(user_id, chat_id, limit) -> list[Message]
    async def delete_messages(user_id, chat_id) -> None
```

**Функция создания пула:**
```python
async def create_connection_pool(database_url: str) -> AsyncConnectionPool
```

**Преимущества:**
- ✅ Простой интерфейс (3 метода)
- ✅ Пул соединений для эффективности
- ✅ Асинхронные методы

### 3. Рефакторинг `ContextManager`

**До (in-memory):**
```python
class ContextManager:
    def __init__(self, max_context_messages: int) -> None:
        self.contexts: dict[tuple[int, int], list[Message]] = {}
```

**После (database):**
```python
class ContextManager:
    def __init__(self, db_repository: DatabaseRepository, max_context_messages: int) -> None:
        self.db_repository = db_repository
        self.max_context_messages = max_context_messages
```

**Изменения:**
- Все методы стали `async`
- Вместо словаря - вызовы `db_repository`
- Логика trimming контекста сохранена

### 4. Обновление `Config` и `main.py`

**Config:**
```python
@dataclass
class Config:
    database_url: str  # NEW: обязательное поле
```

**main.py:**
```python
# Initialize database connection pool
db_pool = await create_connection_pool(config.database_url)
db_repository = DatabaseRepository(db_pool)

context_manager = ContextManager(db_repository, config.max_context_messages)

# ...

finally:
    await db_pool.close()  # Cleanup
```

### 5. Обновление Protocols

**ContextManagerProtocol:**
```python
class ContextManagerProtocol(Protocol):
    async def add_message(...) -> None  # async!
    async def get_context(...) -> list[Message]  # async!
    async def clear_context(...) -> None  # async!
```

Все методы стали асинхронными для совместимости с БД.

## Инфраструктура

### Docker Compose

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: systech_aidd
      POSTGRES_USER: bot_user
      POSTGRES_PASSWORD: bot_password
    ports:
      - "5432:5432"
```

### Yoyo Configuration

```ini
# yoyo.ini
[DEFAULT]
database = postgresql://bot_user:bot_password@localhost:5432/systech_aidd
sources = migrations
```

### Makefile команды

```makefile
db-up:       docker compose up -d postgres
db-down:     docker compose down
db-migrate:  uv run yoyo apply
db-rollback: uv run yoyo rollback
```

## Тестирование

### Стратегия

- **Unit тесты:** Моки `DatabaseRepository` через `AsyncMock`
- **Integration тесты:** (будущее) Testcontainers с реальным PostgreSQL

Все существующие тесты обновлены:
- Добавлена фикстура `mock_db_repository`
- Все методы context_manager теперь `async`
- Проверяем вызовы `save_message`, `get_messages`, `delete_messages`

## Последствия

### Положительные

✅ **Персистентность данных** - история сохраняется между перезапусками  
✅ **Production-ready** - PostgreSQL надежен и масштабируем  
✅ **Простота** - прямой SQL без ORM, легко понять  
✅ **Асинхронность** - полная совместимость с aiogram  
✅ **Версионирование** - Yoyo управляет схемой БД  

### Нейтральные

◽ **Docker dependency** - для локальной разработки нужен Docker  
◽ **Миграции** - нужно запускать `make db-migrate` при изменении схемы  

### Компромиссы

⚠️ **Нет ORM** - пишем SQL руками (но это осознанный выбор для KISS)  
⚠️ **Простая схема** - одна таблица, нет сложных связей (пока достаточно)

## Альтернативные решения (отвергнуты)

### SQLite + aiosqlite
**Почему отвергли:** Проблемы с конкурентностью, сложно масштабировать

### asyncpg вместо psycopg3
**Почему отвергли:** Специфичный API, не DB-API 2.0, больше learning curve

### SQLAlchemy ORM
**Почему отвергли:** Оверинжиниринг, много "магии", нарушение KISS

### Flyway вместо Yoyo
**Почему отвергли:** Требует Java runtime, не Python-native

## Связанные документы

- [ADR-05: Архитектурный рефакторинг (SOLID, DIP, Protocols)](ADR-05.md)
- [Roadmap: Sprint S1](../roadmap.md)
- [Data Model Guide](../guides/04-data-model.md)

---

**Принято:** 2025-10-15  
**Автор:** Архитектурная команда  
**Статус:** Реализовано в Sprint S1




