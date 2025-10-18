# Sprint D0: Basic Docker Setup - План реализации

**Статус:** ✅ Выполнен  
**Дата:** 18 октября 2025

## Обзор

Контейнеризация всех сервисов проекта для запуска полного стека одной командой `docker-compose up`. Фокус на простоте и скорости разработки, без преждевременной оптимизации.

## Цели спринта

1. Создать простые Dockerfile для всех сервисов
2. Настроить docker-compose.yml для оркестрации всех сервисов
3. Обеспечить воспроизводимое локальное окружение для разработки
4. Добавить удобные команды в Makefile для управления Docker

## Реализованные компоненты

### 1. Dockerfile.backend

**Описание:** Простой однослойный образ для Bot и API сервисов

**Характеристики:**
- Базовый образ: `python:3.11-slim`
- Менеджер пакетов: UV (установлен через pip)
- Один образ для двух сервисов (команда переопределяется в docker-compose)
- EXPOSE 8000 для API
- Дефолтная команда: запуск API сервера

**Ключевые решения:**
- ✅ Single-stage build (требование MVP)
- ✅ Без сложной оптимизации
- ✅ Простота и читаемость кода

### 2. Dockerfile.frontend

**Описание:** Простой однослойный образ для Next.js приложения

**Характеристики:**
- Базовый образ: `node:20-slim`
- Менеджер пакетов: pnpm (через corepack)
- Dev-режим для локальной разработки
- EXPOSE 3000
- Hot reload через volume mount

**Ключевые решения:**
- ✅ Single-stage build
- ✅ Dev-режим (production build в следующих спринтах)
- ✅ Простота настройки

### 3. .dockerignore файлы

**backend (.dockerignore.backend):**
- Python кэш (__pycache__, *.pyc)
- Тестовые артефакты (.pytest_cache, .coverage, htmlcov)
- Линтеры (.mypy_cache, .ruff_cache)
- Логи и временные файлы
- Виртуальное окружение (.venv)
- IDE и Git файлы
- Frontend директория

**frontend (.dockerignore.frontend):**
- Node modules
- Next.js build output (.next/, out/)
- Логи
- IDE и Git файлы
- Environment файлы

### 4. docker-compose.yml

**Конфигурация 4 сервисов:**

**postgres** (существующий):
- PostgreSQL 16-alpine
- Healthcheck для зависимостей
- Volume для персистентности данных

**bot** (новый):
- Образ: Dockerfile.backend
- Команда: `uv run python -m src.main`
- Зависит от: postgres (с healthcheck)
- Volume: ./logs:/app/logs
- Переменные окружения из .env

**api** (новый):
- Образ: Dockerfile.backend (тот же что bot)
- Команда: `uv run python -m src.api_server`
- Порты: 8000:8000
- Зависит от: postgres (с healthcheck)
- Volume: ./logs:/app/logs
- Переменные окружения из .env

**frontend** (новый):
- Образ: Dockerfile.frontend
- Команда: `pnpm dev`
- Порты: 3000:3000
- Зависит от: api
- Volume: ./frontend/src:/app/src (hot reload)
- Environment: NEXT_PUBLIC_API_URL=http://localhost:8000

**Сетевая архитектура:**
- Все сервисы в одной bridge сети (default)
- Внутренние DNS имена: postgres, api, bot, frontend
- Внешний доступ: API (8000), Frontend (3000), PostgreSQL (5432)

### 5. Makefile команды

**Добавлены команды для управления Docker:**

| Команда | Описание | Реализация |
|---------|----------|-----------|
| `docker-up` | Запуск всех сервисов | `docker compose up -d` |
| `docker-down` | Остановка сервисов | `docker compose down` |
| `docker-build` | Пересборка образов | `docker compose build --no-cache` |
| `docker-logs` | Логи всех сервисов | `docker compose logs -f` |
| `docker-logs-bot` | Логи Bot | `docker compose logs -f bot` |
| `docker-logs-api` | Логи API | `docker compose logs -f api` |
| `docker-logs-frontend` | Логи Frontend | `docker compose logs -f frontend` |
| `docker-logs-db` | Логи PostgreSQL | `docker compose logs -f postgres` |
| `docker-ps` | Статус сервисов | `docker compose ps` |
| `docker-restart` | Перезапуск | `docker compose restart` |
| `docker-clean` | Полная очистка | `docker compose down -v --rmi all` |

### 6. env.docker.example

**Описание:** Пример файла конфигурации для Docker окружения

**Ключевые особенности:**
- Полная документация всех переменных
- DATABASE_URL с хостом `postgres` (для Docker сети)
- Комментарии на русском языке
- Разделение на логические секции

**Основные переменные:**
- BOT_TOKEN - Telegram bot token
- LLM_API_KEY, LLM_BASE_URL, LLM_MODEL - настройки LLM
- DATABASE_URL - подключение к PostgreSQL (с хостом postgres)
- API_HOST, API_PORT - настройки API сервера
- STAT_COLLECTOR_MODE - режим сбора статистики

### 7. Документация в README.md

**Добавлена секция "🐳 Запуск через Docker":**

1. **Требования** - Docker Desktop установка
2. **Быстрый старт** - пошаговая инструкция:
   - Создание .env файла
   - Запуск сервисов
   - Применение миграций
   - Проверка работоспособности
   - Просмотр логов
   - Остановка
3. **Таблица Docker команд** - полный список команд из Makefile
4. **Структура сервисов** - ASCII диаграмма архитектуры
5. **Полезные советы** - практические примеры использования

## Архитектурные решения

### MVP-подход

✅ **Простота важнее оптимизации:**
- Single-stage Dockerfiles (~20 строк)
- Без hadolint проверок (добавим в D1)
- Без multi-stage builds (добавим в D1)
- Dev-режим для frontend (production в D1)

✅ **Фокус на работоспособности:**
- Один образ для bot и api (переиспользование)
- Простая сетевая конфигурация (default network)
- Явные зависимости через depends_on + healthcheck
- Логи доступны двумя способами (volume + docker logs)

### Зависимости сервисов

```
postgres (healthcheck) 
    ↓
    ├─→ bot (depends_on: postgres)
    └─→ api (depends_on: postgres)
            ↓
        frontend (depends_on: api)
```

### Управление данными

**Volumes:**
- `postgres_data` - персистентность БД
- `./logs` - общие логи для bot и api
- `./frontend/src` - hot reload для frontend

**Миграции:**
- Выполняются вручную при первом запуске
- Команда: `docker compose exec api uv run alembic upgrade head`
- Автоматизация в Sprint D2 (через entrypoint)

## Критерии готовности

### ✅ Функциональные требования

- [x] `docker compose up` запускает все 4 сервиса
- [x] PostgreSQL доступен для bot и api
- [x] API отвечает на http://localhost:8000/docs
- [x] Frontend доступен на http://localhost:3000
- [x] Bot обрабатывает сообщения из Telegram
- [x] Все Makefile команды работают
- [x] Документация обновлена и понятна

### ✅ Технические требования

- [x] Single-stage Dockerfiles для всех сервисов
- [x] .dockerignore файлы настроены
- [x] Правильные depends_on зависимости
- [x] Healthcheck для PostgreSQL
- [x] Volumes для логов и hot reload
- [x] env.docker.example создан
- [x] README.md обновлен с Docker секцией

## План тестирования

**Проверить следующие сценарии:**

1. **Первый запуск:**
   ```bash
   cp env.docker.example .env
   # (заполнить переменные)
   make docker-build
   make docker-up
   docker compose exec api uv run alembic upgrade head
   make docker-ps  # все сервисы running
   ```

2. **Проверка API:**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/docs  # Swagger UI
   ```

3. **Проверка Frontend:**
   ```bash
   curl http://localhost:3000
   # Открыть в браузере
   ```

4. **Проверка Bot:**
   - Отправить сообщение боту в Telegram
   - Получить ответ от LLM
   - Проверить логи: `make docker-logs-bot`

5. **Проверка логов:**
   ```bash
   make docker-logs
   make docker-logs-api
   make docker-logs-bot
   make docker-logs-frontend
   ```

6. **Перезапуск:**
   ```bash
   make docker-restart
   make docker-ps
   ```

7. **Остановка:**
   ```bash
   make docker-down
   make docker-ps  # все остановлены
   ```

## Известные ограничения MVP

1. **Hot reload backend** - не работает (требует перезапуск контейнера)
2. **Миграции** - выполняются вручную (автоматизация в D2)
3. **Логирование** - базовое (улучшенное логирование в будущих спринтах)
4. **Оптимизация образов** - не выполнена (multi-stage в D1)
5. **Security** - базовая (hardening в будущих спринтах)

## Следующие шаги (Sprint D1)

1. Multi-stage builds для оптимизации размера образов
2. Hadolint проверки в CI/CD
3. Production build для frontend
4. GitHub Actions для автоматической сборки
5. Публикация образов в GitHub Container Registry

## Файлы проекта

### Созданные файлы:
- `/Dockerfile.backend` - Docker образ для bot и api
- `/Dockerfile.frontend` - Docker образ для frontend
- `/.dockerignore.backend` - исключения для backend
- `/.dockerignore.frontend` - исключения для frontend
- `/env.docker.example` - пример конфигурации для Docker

### Обновленные файлы:
- `/docker-compose.yml` - добавлены сервисы bot, api, frontend
- `/Makefile` - добавлены Docker команды
- `/README.md` - добавлена секция "🐳 Запуск через Docker"

### Документация:
- `/devops/doc/plans/sprint-d0-docker-setup.md` - этот план
- `/devops/doc/devops-roadmap.md` - обновлен статус Sprint D0

## Выводы

Sprint D0 успешно реализован. Достигнуты все цели:

✅ **Простота** - Dockerfile короткие и понятные (~20 строк)  
✅ **Работоспособность** - все сервисы запускаются одной командой  
✅ **Документация** - подробные инструкции в README  
✅ **Удобство** - Makefile команды для всех операций  
✅ **MVP-подход** - фокус на скорости, а не на оптимизации

Проект готов к следующему спринту (D1: Build & Publish).

