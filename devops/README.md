# DevOps Infrastructure

DevOps инфраструктура для проекта systech-aidd-live.

## Обзор

Реализация DevOps процессов для контейнеризации, CI/CD и автоматического развертывания приложения.

**Подход:** MVP-first - простота и скорость важнее преждевременной оптимизации.

## Текущий статус

### ✅ Sprint D0: Basic Docker Setup (Выполнен)

**Реализовано:**
- Контейнеризация всех сервисов (bot, api, frontend, postgres)
- Docker Compose конфигурация для оркестрации
- Makefile команды для управления Docker
- Документация и примеры конфигурации

**Результат:**
Весь стек запускается одной командой:
```bash
make docker-up
```

**Документация:**
- [Sprint D0 Plan](doc/plans/sprint-d0-docker-setup.md) - детальный план
- [DOCKER-SETUP-SUMMARY.md](../DOCKER-SETUP-SUMMARY.md) - краткое руководство
- [README.md](../README.md#-запуск-через-docker) - секция Docker в главном README

### 🔵 Следующие спринты

- **D1: Build & Publish** - GitHub Actions + Container Registry (запланирован)
- **D2: Развертывание на сервер** - SSH деплой, инструкции (запланирован)
- **D3: Auto Deploy** - автоматический деплой по кнопке (запланирован)

## Структура директории

```
devops/
├── README.md                    # Этот файл
├── doc/
│   ├── devops-roadmap.md       # Roadmap всех DevOps спринтов
│   ├── plans/                  # Детальные планы каждого спринта
│   │   └── sprint-d0-docker-setup.md
│   └── guides/                 # Пошаговые инструкции (будут добавлены)
└── scripts/                    # Скрипты автоматизации (будут добавлены)
```

## Архитектура сервисов

### Docker Compose Stack

```
┌─────────────────┐
│    Frontend     │  Port: 3000
│   (Next.js)     │  Image: systech-aidd-frontend
└────────┬────────┘
         │
         ↓
┌─────────────────┐      ┌─────────────────┐
│      API        │      │      Bot        │
│   (FastAPI)     │  ←─→ │   (aiogram)     │
│  Port: 8000     │      │                 │
│  Image:         │      │  Image:         │
│  backend        │      │  backend        │
└────────┬────────┘      └────────┬────────┘
         │                        │
         └───────────┬────────────┘
                     ↓
         ┌─────────────────┐
         │   PostgreSQL    │  Port: 5432
         │  (16-alpine)    │  Image: postgres:16-alpine
         └─────────────────┘
```

### Ключевые решения

**MVP подход:**
- Single-stage Dockerfiles (простота)
- Один образ для bot и api (переиспользование)
- Dev-режим для frontend (быстрая разработка)
- Без сложной оптимизации (пока)

**Сетевое взаимодействие:**
- Все сервисы в одной bridge сети
- Внутренние DNS имена: postgres, api, bot, frontend
- Внешний доступ: API (8000), Frontend (3000), PostgreSQL (5432)

**Данные:**
- Volume для PostgreSQL (персистентность)
- Volume для логов (bot, api)
- Volume для hot reload (frontend src)

## Быстрый старт

### 1. Подготовка окружения

```bash
# Установить Docker Desktop
# macOS:
brew install --cask docker

# Или скачать: https://www.docker.com/products/docker-desktop
```

### 2. Конфигурация

```bash
# Скопировать пример
cp env.docker.example .env

# Отредактировать .env
# - BOT_TOKEN (от @BotFather)
# - LLM_API_KEY (OpenRouter/OpenAI)
# - LLM_BASE_URL
# - LLM_MODEL
```

### 3. Запуск

```bash
# Запустить все сервисы
make docker-up

# Применить миграции (первый запуск)
docker compose exec api uv run alembic upgrade head

# Проверить статус
make docker-ps
```

### 4. Проверка

- API: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Bot: отправить сообщение в Telegram

### 5. Управление

```bash
# Логи
make docker-logs              # все сервисы
make docker-logs-api          # только API
make docker-logs-bot          # только Bot

# Перезапуск
make docker-restart

# Остановка
make docker-down
```

## Доступные команды

Все команды доступны через Makefile:

| Команда | Описание |
|---------|----------|
| `make docker-up` | Запуск всех сервисов (detached) |
| `make docker-down` | Остановка всех сервисов |
| `make docker-build` | Пересборка образов (no cache) |
| `make docker-logs` | Логи всех сервисов |
| `make docker-logs-bot` | Логи Bot |
| `make docker-logs-api` | Логи API |
| `make docker-logs-frontend` | Логи Frontend |
| `make docker-logs-db` | Логи PostgreSQL |
| `make docker-ps` | Статус всех сервисов |
| `make docker-restart` | Перезапуск всех сервисов |
| `make docker-clean` | Полная очистка (⚠️ удаляет volumes) |

## Конфигурационные файлы

### Dockerfile.backend

**Расположение:** `/Dockerfile.backend`

Образ для Bot и API сервисов:
- Базовый образ: `python:3.11-slim`
- Менеджер пакетов: UV
- Установка зависимостей через `uv sync`
- Копирование кода (src/, prompts/, alembic/)
- EXPOSE 8000

### Dockerfile.frontend

**Расположение:** `/Dockerfile.frontend`

Образ для Frontend:
- Базовый образ: `node:20-slim`
- Менеджер пакетов: pnpm (через corepack)
- Установка зависимостей через `pnpm install`
- Копирование кода (src/, public/, конфиги)
- EXPOSE 3000
- Команда: `pnpm dev`

### docker-compose.yml

**Расположение:** `/docker-compose.yml`

Оркестрация 4 сервисов:
- postgres (база данных с healthcheck)
- bot (зависит от postgres)
- api (зависит от postgres, порт 8000)
- frontend (зависит от api, порт 3000)

### .dockerignore

**Файлы:**
- `/.dockerignore.backend` - исключения для Python проекта
- `/.dockerignore.frontend` - исключения для Next.js проекта

## Переменные окружения

### Обязательные

```bash
BOT_TOKEN=...                    # Telegram bot token
LLM_API_KEY=...                  # OpenRouter/OpenAI API key
LLM_BASE_URL=...                 # LLM provider URL
LLM_MODEL=...                    # Model name
```

### Docker-специфичные

```bash
# ВАЖНО: Используйте хост 'postgres' для Docker
DATABASE_URL=postgresql+asyncpg://systech_user:systech_password@postgres:5432/systech_aidd
```

### Опциональные

```bash
MAX_CONTEXT_MESSAGES=20          # Размер контекста
DATABASE_ECHO=False              # SQL логи
API_HOST=0.0.0.0                 # API хост
API_PORT=8000                    # API порт
STAT_COLLECTOR_MODE=real         # mock или real
```

Полный пример: `env.docker.example`

## Troubleshooting

### Проблемы при сборке

```bash
# Очистить кэш и пересобрать
make docker-clean
make docker-build
make docker-up
```

### Проблемы с PostgreSQL

```bash
# Проверить логи
make docker-logs-db

# Проверить healthcheck
docker compose ps

# Подключиться к БД
docker compose exec postgres psql -U systech_user -d systech_aidd
```

### Проблемы с миграциями

```bash
# Проверить текущую версию
docker compose exec api uv run alembic current

# Применить миграции
docker compose exec api uv run alembic upgrade head

# Откатить миграцию
docker compose exec api uv run alembic downgrade -1
```

### Frontend не подключается к API

Проверьте переменную `NEXT_PUBLIC_API_URL`:
```bash
# В docker-compose.yml должно быть:
environment:
  - NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Документация

### Основная документация

- [DevOps Roadmap](doc/devops-roadmap.md) - план всех спринтов
- [Sprint D0 Plan](doc/plans/sprint-d0-docker-setup.md) - детальный план Sprint D0
- [Docker Setup Summary](../DOCKER-SETUP-SUMMARY.md) - краткое руководство

### Внешние ресурсы

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/dev-best-practices/)

## Следующие шаги

### Sprint D1: Build & Publish

- Multi-stage builds для оптимизации размера образов
- GitHub Actions workflow для автоматической сборки
- Публикация в GitHub Container Registry
- Hadolint проверки для Dockerfile

### Sprint D2: Развертывание на сервер

- Пошаговая инструкция для ручного деплоя
- SSH подключение и авторизация
- Развертывание на production сервере
- Проверка работоспособности

### Sprint D3: Auto Deploy

- GitHub Actions для автоматического деплоя
- Деплой "по кнопке" через workflow_dispatch
- Health checks после деплоя
- Уведомления о статусе

## Контакты

Проект создан в рамках курса **SYSTECH-AIDD-2025**.

---

**Готово к использованию! 🚀**

Начните с:
```bash
make docker-up
```
