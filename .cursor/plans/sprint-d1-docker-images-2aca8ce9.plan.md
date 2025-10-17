<!-- 2aca8ce9-9986-4b5c-b7d2-6977608a0d82 7a6b908d-2551-49fd-87a7-aea0b02752f6 -->
# Sprint D1: Docker-образы и лучшие практики

## Обзор

Создать production-ready Docker-образы для всех сервисов (Бот, API, Frontend) с применением современных практик контейнеризации, оптимизировать для использования в CI/CD и обеспечить локальную разработку с полной оркестрацией.

## Контекст

- Проект использует плоскую структуру: Бот (`src/main.py`) и API (`src/api/main.py`) делят директорию `/src`
- Python-зависимости управляются через UV (`pyproject.toml`)
- Frontend использует Next.js 15 с pnpm (`frontend/package.json`)
- PostgreSQL 16 уже настроен в `docker-compose.yml`
- Dockerfiles пока не существует
- **Все Docker-файлы размещаются в папке `devops/`**

## Задачи реализации

### 1. Создание .dockerignore файлов

Создать отдельные `.dockerignore` файлы для корня (Python-сервисы) и frontend:

- Корневой `.dockerignore`: исключить `.venv/`, `htmlcov/`, `logs/`, `.env`, `.git/`, `frontend/`, `node_modules/`
- `frontend/.dockerignore`: исключить `node_modules/`, `.next/`, `.env*`, отчёты coverage

### 2. Dockerfile для бота (Telegram)

**Файл:** `devops/Dockerfile.bot`

Multi-stage сборка:

- Этап 1 (builder): Установка UV, синхронизация зависимостей из `pyproject.toml`
- Этап 2 (runtime): Копирование только необходимых файлов, запуск от non-root пользователя
- Build context: корень проекта (для доступа к `src/` и `pyproject.toml`)
- Точка входа: `python -m src.main`
- Health check: проверка существования процесса
- Безопасность: non-root пользователь (`appuser`), минимальный базовый образ (`python:3.11-slim`)

Ключевые оптимизации:

- Кэширование слоёв для UV-зависимостей
- Исключение тестовых файлов и dev-зависимостей в runtime
- Включение alembic-миграций для настройки БД

### 3. Dockerfile для API (FastAPI)

**Файл:** `devops/Dockerfile.api`

Multi-stage сборка:

- Этап 1 (builder): Установка UV, синхронизация зависимостей
- Этап 2 (runtime): Копирование зависимостей + исходников, настройка uvicorn
- Build context: корень проекта
- Точка входа: `uvicorn src.api.main:app --host 0.0.0.0 --port 8000`
- Health check: `curl http://localhost:8000/health`
- Expose порт 8000

Production конфигурация:

- Uvicorn workers через переменную окружения
- Security hardening (non-root, read-only где возможно)
- Включение alembic для миграций

### 4. Dockerfile для Frontend (Next.js)

**Файл:** `devops/Dockerfile.frontend`

Multi-stage сборка (3 этапа):

- Этап 1 (deps): Установка pnpm, копирование package-файлов, установка зависимостей
- Этап 2 (builder): Копирование исходников, запуск `pnpm build` со standalone output
- Этап 3 (runner): Минимальный runtime только со standalone приложением
- Build context: `frontend/`
- Точка входа: `node server.js`
- Expose порт 3000

Оптимизации:

- Использование pnpm для эффективного управления зависимостями
- Next.js standalone output для минимального образа
- Переменные окружения для конфигурации API URL

### 5. Расширение docker-compose.yml

**Файл:** `devops/docker-compose.yml` (переместить существующий и расширить)

Добавить сервисы к существующему postgres:

- `bot`: сборка из `devops/Dockerfile.bot` (context: `.`), зависит от postgres, restart policy
- `api`: сборка из `devops/Dockerfile.api` (context: `.`), зависит от postgres, expose 8000
- `frontend`: сборка из `devops/Dockerfile.frontend` (context: `frontend/`), зависит от api, expose 3000
- Общая сеть для межсервисного взаимодействия
- Переменные окружения через `.env` файл

Конфигурация:

- Health checks для всех сервисов
- Правильный порядок зависимостей (postgres → api/bot → frontend)
- Restart policies для отказоустойчивости

### 6. docker-compose.dev.yml

**Файл:** `devops/docker-compose.dev.yml`

Development override для локальной разработки:

- Volume mounts для hot reload: `../src:/app/src`, `../frontend/app:/app/app`
- Dev-специфичные переменные окружения
- Expose портов для отладки
- Отключение production-оптимизаций

### 7. Документация лучших практик

**Файл:** `doc/adrs/ADR-08.md` - Лучшие практики Docker

Задокументировать решения:

- Обоснование multi-stage builds
- Выбор мер безопасности (non-root, минимальные образы)
- Стратегия кэширования слоёв
- Обработка плоской структуры (shared /src для bot и api)
- Реализация health checks
- Конфигурации для разработки vs production
- Размещение в папке `devops/`

### 8. Настройка сканирования безопасности контейнеров

**Файл:** `devops/.hadolint.yaml`

Добавить в проект:

- Конфигурацию Hadolint для проверки Dockerfile
- Инструкции по сканированию безопасности через Trivy в документации
- Makefile targets: `make docker-lint`, `make docker-scan`

### 9. Документация по сборке и запуску

**Обновить:** `README.md` и создать `doc/guides/09-docker-deployment.md`

Включить:

- Команды сборки: `docker compose -f devops/docker-compose.yml build`
- Команды запуска: `docker compose -f devops/docker-compose.yml up -d`
- Проверка health: `docker compose -f devops/docker-compose.yml ps`
- Просмотр логов: `docker compose -f devops/docker-compose.yml logs -f [service]`
- Остановка сервисов: `docker compose -f devops/docker-compose.yml down`
- Режим разработки: `docker compose -f devops/docker-compose.yml -f devops/docker-compose.dev.yml up`
- Makefile targets для упрощения команд

### 10. Команды Makefile

Добавить новые targets в `Makefile`:

```makefile
make docker-build          # Сборка всех образов
make docker-up             # Запуск всех сервисов
make docker-down           # Остановка всех сервисов
make docker-logs           # Просмотр логов
make docker-clean          # Удаление образов и volumes
make docker-lint           # Проверка Hadolint
make docker-scan           # Сканирование безопасности Trivy
make docker-dev            # Запуск в dev режиме
```

Команды будут использовать `-f devops/docker-compose.yml` автоматически.

### 11. Адаптация для промышленного использования

**Добавить в ADR-08 и документацию:**

Секция о переходе к публичному registry (Docker Hub, GitHub Container Registry, AWS ECR):

**Что потребуется изменить:**

- `devops/docker-compose.yml`: заменить директивы `build:` на `image:` с указанием полного пути к образам (например, `ghcr.io/org/systech-aidd-bot:latest`)
- Добавить теги версионирования (semver): `v1.0.0`, `v1.0.0-rc.1`, `latest`, `stable`
- CI/CD pipeline: добавить этапы login в registry, тегирования и push образов
- `.env.example`: добавить переменные `REGISTRY_URL`, `IMAGE_TAG` для гибкой конфигурации
- Secrets management: переменные окружения через orchestrator (K8s secrets, Docker secrets)

**Что НЕ потребуется менять:**

- Сами Dockerfile в `devops/` остаются без изменений
- Структура приложения и точки входа
- Health checks и настройки безопасности
- Логика работы сервисов

**Дополнительные рекомендации:**

- Настроить automated builds при push в main/tags
- Добавить image signing для верификации (cosign, Docker Content Trust)
- Настроить vulnerability scanning в CI pipeline
- Документировать процесс rollback к предыдущим версиям
- Добавить мониторинг размеров образов и CI-метрик

## Тестирование и валидация

После реализации:

1. Собрать все образы: `make docker-build`
2. Запустить сервисы: `make docker-up`
3. Проверить health: `curl http://localhost:8000/health`
4. Проверить frontend: `curl http://localhost:3000`
5. Протестировать подключение бота к БД
6. Запустить сканирование безопасности: `make docker-scan`
7. Проверить размеры образов (целевые: API < 200MB, Frontend < 150MB)

## Поставляемые результаты

- [ ] `.dockerignore` (корень и frontend)
- [ ] `devops/Dockerfile.bot` (multi-stage, оптимизированный)
- [ ] `devops/Dockerfile.api` (multi-stage, production-ready)
- [ ] `devops/Dockerfile.frontend` (standalone Next.js)
- [ ] `devops/docker-compose.yml` (полная оркестрация, перемещён из корня)
- [ ] `devops/docker-compose.dev.yml` (development overrides)
- [ ] `doc/adrs/ADR-08.md` (решения по контейнеризации + секция про registry)
- [ ] `doc/guides/09-docker-deployment.md` (руководство по использованию)
- [ ] `devops/.hadolint.yaml` (конфигурация линтера)
- [ ] Обновлённый `Makefile` (Docker-команды с путями к devops/)
- [ ] Обновлённый `README.md` (секция Docker)

### To-dos

- [ ] Create .dockerignore files for root and frontend directories
- [ ] Create Dockerfile.bot with multi-stage build for Telegram bot
- [ ] Create Dockerfile.api with multi-stage build for FastAPI service
- [ ] Create frontend/Dockerfile with standalone Next.js build
- [ ] Extend docker-compose.yml to orchestrate all services (bot, api, frontend, postgres)
- [ ] Create docker-compose.dev.yml for development overrides with volume mounts
- [ ] Add .hadolint.yaml and document Trivy scanning setup
- [ ] Document Docker containerization decisions in ADR-08
- [ ] Add Docker-related commands to Makefile (build, up, down, logs, clean, lint, scan)
- [ ] Create deployment guide and update README with Docker instructions
- [ ] Test full Docker setup: build, run, health checks, and security scans