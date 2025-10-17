# Makefile для systech-aidd-live
#
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
# Команды для API:
#   make api-run            - запуск API сервера (uvicorn)
#   make api-test           - тестирование API endpoints (curl)
#   make api-docs           - открыть Swagger UI документацию
#
# Команды для Frontend:
#   make frontend-install   - установка frontend зависимостей (pnpm)
#   make frontend-dev       - запуск frontend dev сервера
#   make frontend-build     - production build frontend
#   make frontend-start     - запуск frontend production сервера
#   make frontend-lint      - проверка frontend кода (ESLint)
#   make frontend-lint-fix  - автоматическое исправление frontend lint ошибок
#   make frontend-format    - форматирование frontend кода (Prettier)
#   make frontend-format-check - проверка frontend форматирования
#   make frontend-type-check - проверка типов TypeScript
#   make frontend-check-all - все проверки frontend (lint + format + types)
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
# Утилиты:
#   make clean              - очистка логов и временных файлов
#   make dev                - запуск API и Frontend одновременно (full stack dev)
#
.PHONY: install run test test-cov test-all test-integration format lint check-all clean
.PHONY: db-up db-down db-migrate db-rollback db-revision db-shell db-logs
.PHONY: api-run api-test api-docs
.PHONY: frontend-install frontend-dev frontend-build frontend-start frontend-lint frontend-lint-fix frontend-format frontend-format-check frontend-type-check frontend-check-all
.PHONY: dev

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

# API commands
api-run:
	uv run python -m src.api_server

api-test:
	@echo "Testing API endpoints..."
	@curl -s http://localhost:8000/health | python -m json.tool
	@echo "\n---\nTesting statistics (default period=month):"
	@curl -s http://localhost:8000/api/v1/statistics | python -m json.tool
	@echo "\n---\nTesting statistics (period=day):"
	@curl -s "http://localhost:8000/api/v1/statistics?period=day" | python -m json.tool

api-docs:
	@echo "Opening API documentation in browser..."
	@open http://localhost:8000/docs || xdg-open http://localhost:8000/docs || echo "Please open http://localhost:8000/docs in your browser"

# Frontend commands
frontend-install:
	@echo "Installing frontend dependencies..."
	cd frontend && pnpm install

frontend-dev:
	@echo "Starting frontend development server..."
	cd frontend && pnpm dev

frontend-build:
	@echo "Building frontend for production..."
	cd frontend && pnpm build

frontend-start:
	@echo "Starting frontend production server..."
	cd frontend && pnpm start

frontend-lint:
	@echo "Linting frontend code..."
	cd frontend && pnpm lint

frontend-lint-fix:
	@echo "Fixing frontend linting issues..."
	cd frontend && pnpm lint:fix

frontend-format:
	@echo "Formatting frontend code..."
	cd frontend && pnpm format

frontend-format-check:
	@echo "Checking frontend code formatting..."
	cd frontend && pnpm format:check

frontend-type-check:
	@echo "Type checking frontend code..."
	cd frontend && pnpm type-check

frontend-check-all: frontend-lint frontend-format-check frontend-type-check
	@echo "✅ All frontend checks passed!"

# Chat API testing
.PHONY: chat-test
chat-test:
	@echo "Testing chat API (normal mode)..."
	@curl -X POST http://localhost:8000/api/v1/chat/message \
		-H "Content-Type: application/json" \
		-d '{"message": "Hello, how are you?", "mode": "normal", "user_id": 1, "chat_id": 1}' \
		| python3 -m json.tool

.PHONY: chat-test-admin
chat-test-admin:
	@echo "Testing chat API (admin mode with text2sql)..."
	@curl -X POST http://localhost:8000/api/v1/chat/message \
		-H "Content-Type: application/json" \
		-d '{"message": "Сколько всего сообщений в базе данных?", "mode": "admin", "user_id": 1, "chat_id": 1}' \
		| python3 -m json.tool

.PHONY: chat-history
chat-history:
	@echo "Getting chat history..."
	@curl http://localhost:8000/api/v1/chat/history?user_id=1\&chat_id=1\&limit=10 \
		| python3 -m json.tool

# Full stack development
dev:
	@echo "Starting API and Frontend dev servers..."
	@echo "API will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:3000"
	@trap 'kill 0' EXIT; \
	make api-run & \
	make frontend-dev & \
	wait
