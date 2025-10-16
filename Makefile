# Makefile для systech-aidd-live
#
# === BACKEND ===
# Команды для разработки:
#   make install            - установка зависимостей (включая dev-инструменты)
#   make run                - запуск бота
#
# Команды для базы данных:
#   make db-up              - запуск PostgreSQL через Docker Compose
#   make db-down            - остановка PostgreSQL
#   make db-migrate         - применение миграций (alembic upgrade head)
#   make db-rollback        - откат последней миграции
#   make db-revision        - создание новой миграции (указать message="название")
#   make db-shell           - подключение к PostgreSQL через psql
#   make db-logs            - просмотр логов PostgreSQL
#
# Команды для тестирования:
#   make test               - запуск unit тестов (без integration)
#   make test-cov           - запуск тестов с coverage (без integration)
#   make test-integration   - запуск только integration тестов (реальные API вызовы)
#   make test-all           - запуск всех тестов (unit + integration)
#
# Команды для качества кода:
#   make format             - автоформатирование кода (ruff format)
#   make lint               - проверка кода (ruff check + mypy)
#   make check-all          - полная проверка (format + lint + test-cov)
#
# API server:
#   make api-run            - запуск API сервера (production mode)
#   make api-dev            - запуск API сервера (dev mode с hot reload)
#   make api-test           - тест API endpoint (GET /api/stats)
#
# === FRONTEND ===
# Команды для разработки:
#   make frontend-install   - установка зависимостей frontend (pnpm)
#   make frontend-dev       - запуск dev сервера (http://localhost:3000)
#   make frontend-build     - сборка production build
#   make frontend-start     - запуск production сервера
#
# Команды для качества кода:
#   make frontend-lint      - проверка кода (ESLint)
#   make frontend-format    - форматирование кода (Prettier)
#   make frontend-type-check - проверка типов (TypeScript)
#   make frontend-check-all - полная проверка (format + lint + type-check)
#
# Утилиты:
#   make clean              - очистка логов и временных файлов
#
.PHONY: help install run test test-cov test-all test-integration format lint check-all clean
.PHONY: db-up db-down db-migrate db-rollback db-revision db-shell db-logs
.PHONY: api-run api-dev api-test
.PHONY: frontend-install frontend-dev frontend-build frontend-start
.PHONY: frontend-lint frontend-format frontend-type-check frontend-check-all

.DEFAULT_GOAL := help

help:
	@echo "systech-aidd-live - Makefile commands"
	@echo ""
	@echo "=== BACKEND ==="
	@echo "Development:"
	@echo "  make install            - установка зависимостей (включая dev-инструменты)"
	@echo "  make run                - запуск бота"
	@echo ""
	@echo "Database:"
	@echo "  make db-up              - запуск PostgreSQL через Docker Compose"
	@echo "  make db-down            - остановка PostgreSQL"
	@echo "  make db-migrate         - применение миграций (alembic upgrade head)"
	@echo "  make db-rollback        - откат последней миграции"
	@echo "  make db-revision        - создание новой миграции (message=\"название\")"
	@echo "  make db-shell           - подключение к PostgreSQL через psql"
	@echo "  make db-logs            - просмотр логов PostgreSQL"
	@echo ""
	@echo "Testing:"
	@echo "  make test               - запуск unit тестов (без integration)"
	@echo "  make test-cov           - запуск тестов с coverage (без integration)"
	@echo "  make test-integration   - запуск только integration тестов"
	@echo "  make test-all           - запуск всех тестов (unit + integration)"
	@echo ""
	@echo "Code quality:"
	@echo "  make format             - автоформатирование кода (ruff format)"
	@echo "  make lint               - проверка кода (ruff check + mypy)"
	@echo "  make check-all          - полная проверка (format + lint + test-cov)"
	@echo ""
	@echo "API server:"
	@echo "  make api-run            - запуск API сервера (production mode)"
	@echo "  make api-dev            - запуск API сервера (dev mode с hot reload)"
	@echo "  make api-test           - тест API endpoint (GET /api/stats)"
	@echo ""
	@echo "=== FRONTEND ==="
	@echo "Development:"
	@echo "  make frontend-install   - установка зависимостей frontend (pnpm)"
	@echo "  make frontend-dev       - запуск dev сервера (http://localhost:3000)"
	@echo "  make frontend-build     - сборка production build"
	@echo "  make frontend-start     - запуск production сервера"
	@echo ""
	@echo "Code quality:"
	@echo "  make frontend-lint      - проверка кода (ESLint)"
	@echo "  make frontend-format    - форматирование кода (Prettier)"
	@echo "  make frontend-type-check - проверка типов (TypeScript)"
	@echo "  make frontend-check-all - полная проверка (format + lint + type-check)"
	@echo ""
	@echo "=== UTILITIES ==="
	@echo "  make clean              - очистка логов и временных файлов"
	@echo "  make help               - показать эту справку"

install:
	uv sync --extra dev

run:
	uv run python -m src.main

test:
	uv run pytest tests/ -v -m "not integration"

test-cov:
	uv run pytest -m "not integration"

test-integration:
	uv run pytest tests/ -v -m "integration"

test-all:
	uv run pytest tests/ -v

format:
	uv run ruff format src/ tests/

lint:
	uv run ruff check src/ tests/
	uv run mypy src/ tests/

check-all: format lint test-cov

clean:
	rm -rf logs/*.log htmlcov/ .coverage .pytest_cache .mypy_cache .ruff_cache

# Database commands
db-up:
	docker compose up -d postgres

db-down:
	docker compose down

db-migrate:
	uv run alembic upgrade head

db-rollback:
	uv run alembic downgrade -1

db-revision:
	uv run alembic revision --autogenerate -m "$(message)"

db-shell:
	docker compose exec postgres psql -U systech_user -d systech_aidd

db-logs:
	docker compose logs -f postgres

# API server commands (separate from bot)
api-run:
	uv run python -m src.api.main

api-dev:
	uv run uvicorn src.api.server:app --reload --port 8000

api-test:
	curl -s http://localhost:8000/api/stats | python -m json.tool

# Frontend commands
frontend-install:
	cd frontend && pnpm install

frontend-dev:
	cd frontend && pnpm dev

frontend-build:
	cd frontend && pnpm build

frontend-start:
	cd frontend && pnpm start

frontend-lint:
	cd frontend && pnpm lint

frontend-format:
	cd frontend && pnpm format

frontend-type-check:
	cd frontend && pnpm type-check

frontend-check-all: frontend-format frontend-lint frontend-type-check
