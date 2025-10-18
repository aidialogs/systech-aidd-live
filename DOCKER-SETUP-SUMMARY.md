# Sprint D0: Basic Docker Setup - Резюме

**Статус:** ✅ Выполнен  
**Дата:** 18 октября 2025

## Что реализовано

### 🐳 Контейнеризация всех сервисов

Теперь весь стек запускается **одной командой**:

```bash
make docker-up
```

### 📦 Созданные файлы

1. **Dockerfile.backend** - образ для Bot и API (Python 3.11 + UV)
2. **Dockerfile.frontend** - образ для Frontend (Node.js 20 + pnpm)
3. **.dockerignore.backend** - исключения для Python проекта
4. **.dockerignore.frontend** - исключения для Next.js проекта
5. **env.docker.example** - пример конфигурации для Docker окружения

### 🔄 Обновленные файлы

1. **docker-compose.yml** - добавлены сервисы bot, api, frontend
2. **Makefile** - добавлены 11 Docker команд
3. **README.md** - добавлена секция "🐳 Запуск через Docker"

## Быстрый старт

### 1. Подготовка

```bash
# Скопировать пример конфигурации
cp env.docker.example .env

# Отредактировать .env (заполнить BOT_TOKEN, LLM_API_KEY, и т.д.)
```

### 2. Запуск

```bash
# Запустить все сервисы
make docker-up

# Применить миграции БД (только первый раз)
docker compose exec api uv run alembic upgrade head

# Проверить статус
make docker-ps
```

### 3. Проверка

- **API**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **Bot**: отправить сообщение в Telegram

### 4. Логи

```bash
make docker-logs           # все сервисы
make docker-logs-api       # только API
make docker-logs-bot       # только Bot
make docker-logs-frontend  # только Frontend
```

### 5. Остановка

```bash
make docker-down
```

## Архитектура

```
┌─────────────┐
│  Frontend   │ :3000
│  (Next.js)  │
└──────┬──────┘
       │
       ↓
┌─────────────┐     ┌─────────────┐
│     API     │←────│     Bot     │
│  (FastAPI)  │:8000│  (aiogram)  │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └───────┬───────────┘
               ↓
       ┌─────────────┐
       │ PostgreSQL  │ :5432
       └─────────────┘
```

## Доступные команды

| Команда | Описание |
|---------|----------|
| `make docker-up` | Запуск всех сервисов |
| `make docker-down` | Остановка всех сервисов |
| `make docker-build` | Пересборка образов |
| `make docker-logs` | Просмотр логов всех сервисов |
| `make docker-logs-bot` | Логи Bot |
| `make docker-logs-api` | Логи API |
| `make docker-logs-frontend` | Логи Frontend |
| `make docker-logs-db` | Логи PostgreSQL |
| `make docker-ps` | Статус сервисов |
| `make docker-restart` | Перезапуск всех сервисов |
| `make docker-clean` | Полная очистка |

## Особенности реализации

### MVP-подход

✅ **Простота**
- Single-stage Dockerfiles (~20 строк)
- Без multi-stage builds
- Без сложной оптимизации

✅ **Работоспособность**
- Один образ для bot и api
- Простая сетевая конфигурация
- Явные зависимости через depends_on

✅ **Удобство**
- Все команды через Makefile
- Hot reload для frontend
- Логи доступны двумя способами

### Технические детали

**Backend (Bot + API):**
- Базовый образ: `python:3.11-slim`
- Менеджер пакетов: UV
- Порт: 8000 (только для API)
- Volume: `./logs` для персистентных логов

**Frontend:**
- Базовый образ: `node:20-slim`
- Менеджер пакетов: pnpm
- Порт: 3000
- Volume: `./frontend/src` для hot reload

**PostgreSQL:**
- Образ: `postgres:16-alpine`
- Порт: 5432
- Volume: `postgres_data` для персистентности
- Healthcheck для зависимостей

## Важные замечания

### 🔑 DATABASE_URL для Docker

В Docker окружении используйте хост `postgres` вместо `localhost`:

```bash
# ❌ Неправильно (для локального запуска)
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db

# ✅ Правильно (для Docker)
DATABASE_URL=postgresql+asyncpg://user:pass@postgres:5432/db
```

Это уже настроено в `env.docker.example`.

### 🔄 Миграции БД

При первом запуске выполните миграции:

```bash
docker compose exec api uv run alembic upgrade head
```

В будущих спринтах это будет автоматизировано.

### 🔥 Hot Reload

- **Frontend**: работает (через volume mount)
- **Backend**: не работает (требует перезапуск контейнера)

Для перезапуска backend:
```bash
make docker-restart
```

## Что дальше?

### Sprint D1: Build & Publish

- Multi-stage builds для оптимизации
- GitHub Actions для автоматической сборки
- Публикация образов в GitHub Container Registry
- Hadolint проверки

### Sprint D2: Развертывание на сервер

- Инструкция для ручного деплоя
- SSH подключение
- Развертывание на production сервере

### Sprint D3: Auto Deploy

- Автоматический деплой через GitHub Actions
- Деплой "по кнопке"
- Health checks после деплоя

## Документация

- **Детальный план**: [devops/doc/plans/sprint-d0-docker-setup.md](devops/doc/plans/sprint-d0-docker-setup.md)
- **DevOps Roadmap**: [devops/doc/devops-roadmap.md](devops/doc/devops-roadmap.md)
- **README.md**: Секция "🐳 Запуск через Docker"

## Критерии готовности

- [x] `docker compose up` запускает все 4 сервиса
- [x] PostgreSQL доступен для bot и api
- [x] API отвечает на http://localhost:8000/docs
- [x] Frontend доступен на http://localhost:3000
- [x] Bot обрабатывает сообщения из Telegram
- [x] Все Makefile команды работают
- [x] Документация обновлена

---

**Готово к использованию! 🚀**

Попробуйте запустить:
```bash
make docker-up
```

