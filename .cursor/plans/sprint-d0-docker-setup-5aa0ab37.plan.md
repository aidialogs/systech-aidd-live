<!-- 5aa0ab37-4da6-4cf6-97c1-cbf43a08b024 75403729-1749-472d-b649-33f0c779b2d8 -->
# План Sprint D0: Basic Docker Setup

## Обзор

Создать простую Docker-инфраструктуру для локального запуска всех сервисов проекта одной командой. Фокус на скорости и простоте, без преждевременной оптимизации.

## Файловая структура

Все Docker-файлы будут созданы в корне проекта:

```
/
├── Dockerfile.backend         # Для bot и api сервисов
├── Dockerfile.frontend        # Для Next.js приложения
├── .dockerignore.backend      # Исключения для backend
├── .dockerignore.frontend     # Исключения для frontend
└── docker-compose.yml         # Обновленная конфигурация всех сервисов
```

## Детали реализации

### 1. Dockerfile.backend (Python + UV)

Простой однослойный образ на базе Python 3.11:

- Установка uv через pip
- Копирование pyproject.toml и uv.lock
- Установка зависимостей через `uv sync`
- Копирование исходного кода (src/, prompts/, alembic/)
- Рабочая директория `/app`
- EXPOSE 8000 (для API)
- Дефолтный CMD: `["uv", "run", "python", "-m", "src.api_server"]`

**Ключевые решения:**

- Используем официальный образ `python:3.11-slim`
- Один образ для bot и api (CMD переопределяется для bot через docker-compose)
- Без multi-stage builds (требование MVP)
- EXPOSE 8000 явно указан (best practice)
- Дефолтная команда запускает API (для bot переопределится в docker-compose)

### 2. Dockerfile.frontend (Node.js + pnpm)

Простой однослойный образ на базе Node.js 20:

- Установка pnpm через corepack
- Копирование package.json и pnpm-lock.yaml
- Установка зависимостей
- Копирование исходного кода (frontend/src/, frontend/public/, конфиги)
- Запуск dev-сервера для локальной разработки

**Ключевые решения:**

- Используем официальный образ `node:20-slim`
- Dev-режим для локальной разработки (production build - в следующих спринтах)
- Порт 3000 будет проброшен в docker-compose

### 3. .dockerignore файлы

**backend (.dockerignore.backend):**

```
# Python
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# Logs and temp
logs/
*.log
.env

# Dev tools
.venv/
.vscode/
.git/
```

**frontend (.dockerignore.frontend):**

```
# Node
node_modules/
.next/
out/

# Build artifacts
*.tsbuildinfo

# Logs
*.log

# Dev
.vscode/
.git/
.env
```

### 4. docker-compose.yml

Расширение существующего файла для добавления 3 новых сервисов:

**postgres** (уже существует) - без изменений

**bot** (новый сервис):

- Образ: собирается из Dockerfile.backend
- Команда: `uv run python -m src.main`
- Зависит от: postgres (with condition: service_healthy)
- Переменные окружения из .env
- Volume для логов: `./logs:/app/logs`
- restart: unless-stopped

**api** (новый сервис):

- Образ: собирается из Dockerfile.backend (тот же что bot)
- Команда: `uv run python -m src.api_server`
- Порты: 8000:8000
- Зависит от: postgres (with condition: service_healthy)
- Переменные окружения из .env
- Volume для логов: `./logs:/app/logs`
- restart: unless-stopped

**frontend** (новый сервис):

- Образ: собирается из Dockerfile.frontend
- Команда: `pnpm dev`
- Порты: 3000:3000
- Зависит от: api
- Переменные окружения: NEXT_PUBLIC_API_URL=http://api:8000
- Volume для hot-reload: `./frontend/src:/app/src`
- restart: unless-stopped

**Сеть:**

- Все сервисы в одной bridge сети (default)
- Внутренние DNS имена: postgres, api, bot, frontend

### 5. Обновление Makefile

Добавить новую секцию Docker Commands:

```makefile
# Docker commands
docker-up:                     # Запуск всех сервисов
docker-down:                   # Остановка всех сервисов
docker-build:                  # Пересборка образов
docker-logs:                   # Логи всех сервисов
docker-logs-bot:               # Логи бота
docker-logs-api:               # Логи API
docker-logs-frontend:          # Логи frontend
docker-logs-db:                # Логи PostgreSQL
docker-ps:                     # Статус сервисов
docker-restart:                # Перезапуск всех сервисов
docker-clean:                  # Полная очистка (containers + volumes + images)
```

**Реализация команд:**

- `docker-up`: `docker compose up -d` (detached mode)
- `docker-down`: `docker compose down`
- `docker-build`: `docker compose build --no-cache`
- `docker-logs`: `docker compose logs -f`
- `docker-logs-{service}`: `docker compose logs -f {service}`
- `docker-ps`: `docker compose ps`
- `docker-restart`: `docker compose restart`
- `docker-clean`: `docker compose down -v --rmi all`

### 6. Обновление README.md

Добавить новую секцию "🐳 Запуск через Docker" после секции "Быстрый старт":

**Содержание секции:**

1. Требования (Docker + Docker Compose)
2. Подготовка .env файла
3. Запуск: `make docker-up` или `docker compose up`
4. Проверка работоспособности (доступ к сервисам)
5. Просмотр логов
6. Остановка сервисов
7. Список всех Docker команд из Makefile

**Структура документации:**

````markdown
## 🐳 Запуск через Docker

Самый простой способ запустить весь стек сервисов локально.

### Требования
- Docker Desktop (или Docker Engine + Docker Compose)

### Быстрый старт

1. Создайте .env файл (скопируйте из .env.example)
2. Запустите все сервисы:
   ```bash
   make docker-up
   # или
   docker compose up
   ```

3. Проверьте доступность:
   - API: http://localhost:8000/docs
   - Frontend: http://localhost:3000
   - Bot: проверьте логи через `make docker-logs-bot`

4. Просмотр логов:
   ```bash
   make docker-logs          # все сервисы
   make docker-logs-api      # только API
   make docker-logs-bot      # только Bot
   ```

5. Остановка:
   ```bash
   make docker-down
   ```

### Доступные команды

[таблица команд из Makefile]
````

### 7. Создание .env.example.docker

Создать файл с примером переменных для Docker-окружения:

- DATABASE_URL с хостом `postgres` (внутреннее имя в Docker сети)
- Все остальные переменные из существующего .env.example

## Важные детали

**Миграции БД:**

- При первом запуске нужно выполнить миграции вручную:
  ```bash
  docker compose exec api uv run alembic upgrade head
  ```

- В будущих спринтах автоматизируем через entrypoint script

**Hot Reload:**

- Frontend: работает через volume mount `./frontend/src:/app/src`
- Backend: не реализован в MVP (требует перезапуск контейнера)

**Логи:**

- Volume `./logs:/app/logs` для персистентности логов
- Также доступны через `docker compose logs`

**Зависимости сервисов:**

- bot и api ждут PostgreSQL healthcheck
- frontend ждет запуска api (depends_on)

## Критерии готовности

✅ Команда `docker compose up` запускает все 4 сервиса

✅ PostgreSQL доступен для bot и api

✅ API отвечает на http://localhost:8000/docs

✅ Frontend доступен на http://localhost:3000

✅ Bot обрабатывает сообщения из Telegram

✅ Все Makefile команды работают

✅ Документация обновлена и понятна

## Тестирование

После реализации проверить:

1. `make docker-up` - запуск всех сервисов
2. `make docker-ps` - все сервисы в статусе "running"
3. `curl http://localhost:8000/health` - API отвечает
4. `curl http://localhost:3000` - Frontend отвечает
5. Отправить сообщение боту в Telegram - получить ответ
6. `make docker-logs-api` - логи отображаются
7. `make docker-down` - остановка всех сервисов

### To-dos

- [ ] Создать Dockerfile.backend и Dockerfile.frontend с простой конфигурацией (без multi-stage)
- [ ] Создать .dockerignore.backend и .dockerignore.frontend для исключения ненужных файлов
- [ ] Обновить docker-compose.yml для добавления сервисов bot, api, frontend с правильными зависимостями
- [ ] Добавить Docker команды в Makefile (up, down, build, logs, ps, restart, clean)
- [ ] Создать .env.example.docker с переменными для Docker окружения
- [ ] Обновить README.md с секцией по запуску через Docker и всеми командами
- [ ] Протестировать полный цикл: сборка, запуск, проверка работы всех сервисов, остановка