<!-- a53d272e-178d-4634-b116-331bc8ca1b26 d659f6e6-6265-4d3e-b268-4e69cde06770 -->
# Sprint S1: Persistent Storage with PostgreSQL

## Технический стек

- PostgreSQL (через Docker)
- psycopg3 (асинхронный драйвер)
- Yoyo (миграции на чистом SQL)
- Прямые SQL запросы (без ORM)

## Схема базы данных

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
```

## Архитектурные изменения

### 1. Новый модуль: `src/database.py`

Простой репозиторий с методами:

- `async def save_message(user_id, chat_id, role, content)` - сохранение сообщения
- `async def get_messages(user_id, chat_id, limit)` - получение истории
- `async def delete_messages(user_id, chat_id)` - очистка контекста

### 2. Модификация `src/context_manager.py`

- Удалить `self.contexts: dict` (in-memory хранилище)
- Добавить `self.db_pool: AsyncConnectionPool` (пул соединений psycopg3)
- Методы будут делегировать вызовы к БД через `database.py`

### 3. Обновление `src/config.py`

Добавить поля для PostgreSQL:

```python
database_url: str  # postgresql://user:pass@host:5432/dbname
```

### 4. Обновление `src/main.py`

- Создать пул соединений при старте
- Передать пул в ContextManager
- Закрыть пул при остановке

## Инфраструктура

### Docker Compose

Файл `docker-compose.yml`:

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
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### Yoyo миграции

Директория `migrations/`:

- `001_initial_schema.sql` - создание таблицы messages

## Изменения в тестах

### Стратегия тестирования

- Unit тесты: использовать testcontainers для реального PostgreSQL
- Или: мокировать пул соединений для быстрых тестов
- Integration тест: полный flow с реальной БД

Файлы для обновления:

- `tests/test_context_manager.py` - адаптировать под async и БД
- `tests/test_database.py` (новый) - тесты репозитория
- `tests/conftest.py` - добавить фикстуру для БД

## Документация

### ADR-06: Выбор технологий для персистентного хранения

Документировать решение использовать PostgreSQL + psycopg3 + Yoyo

### Обновить документацию

- `doc/guides/01-getting-started.md` - добавить инструкции по запуску PostgreSQL
- `README.md` - обновить requirements

## Makefile команды

Добавить новые команды:

```makefile
db-up:       docker compose up -d postgres
db-down:     docker compose down
db-migrate:  yoyo apply
db-rollback: yoyo rollback
```

## Ключевые файлы для изменения

1. `pyproject.toml` - добавить psycopg[binary], yoyo-migrations
2. `src/database.py` - новый модуль (репозиторий)
3. `src/context_manager.py` - рефакторинг (убрать dict, добавить БД)
4. `src/config.py` - добавить DATABASE_URL
5. `src/main.py` - инициализация пула соединений
6. `docker-compose.yml` - новый файл
7. `migrations/001_initial_schema.sql` - новый файл
8. `.env.example` - добавить DATABASE_URL (создать файл)
9. `tests/test_context_manager.py` - адаптировать под async
10. `tests/test_database.py` - новый файл
11. `doc/adrs/ADR-06.md` - новый файл

## Принцип KISS

- Одна таблица, простая схема
- Прямые SQL запросы без абстракций
- Минимум новых зависимостей (2 пакета)
- Простой репозиторий без сложной логики
- Docker для локальной разработки

### To-dos

- [ ] Setup infrastructure: Docker Compose, add dependencies to pyproject.toml, create .env.example
- [ ] Create Yoyo migrations: initial schema with messages table and indexes
- [ ] Implement src/database.py: connection pool helper and repository functions for CRUD operations
- [ ] Refactor src/context_manager.py: replace in-memory dict with database calls
- [ ] Update src/config.py and src/main.py: add DATABASE_URL config, initialize connection pool
- [ ] Update tests: adapt test_context_manager.py for async, create test_database.py, update conftest.py
- [ ] Update Makefile: add db-up, db-down, db-migrate, db-rollback commands
- [ ] Create ADR-06, update README.md and getting-started guide with PostgreSQL setup instructions