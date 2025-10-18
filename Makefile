# Makefile для systech-aidd-live
#
# Используйте 'make help' для просмотра всех доступных команд
#
.PHONY: help install run test test-cov test-all test-integration format lint check-all clean
.PHONY: db-up db-down db-migrate db-rollback db-revision db-shell db-logs
.PHONY: api-run api-docs api-test
.PHONY: frontend-install frontend-dev frontend-build frontend-start frontend-lint frontend-format frontend-type-check frontend-check-all
.PHONY: docker-build docker-up docker-down docker-logs docker-ps docker-clean docker-dev docker-lint docker-scan docker-restart
.PHONY: ci-lint-backend ci-lint-frontend ci-test ci-build ci-check-all

# Default target
.DEFAULT_GOAL := help

# NVM setup для frontend команд
NVM_DIR := $(HOME)/.nvm
NVM_SH := $(NVM_DIR)/nvm.sh
WITH_NVM := source $(NVM_SH) && nvm use default &&

help: ## Показать это сообщение с помощью
	@echo "Доступные команды:"
	@echo ""
	@echo "Backend:"
	@echo "  make install            - установка зависимостей (uv sync)"
	@echo "  make run                - запуск Telegram бота"
	@echo ""
	@echo "API сервер:"
	@echo "  make api-run            - запуск FastAPI сервера (порт 8000)"
	@echo "  make api-docs           - показать ссылки на документацию API"
	@echo "  make api-test           - тестирование API endpoints"
	@echo ""
	@echo "База данных:"
	@echo "  make db-up              - запуск PostgreSQL (Docker)"
	@echo "  make db-down            - остановка PostgreSQL"
	@echo "  make db-migrate         - применение миграций"
	@echo "  make db-rollback        - откат последней миграции"
	@echo "  make db-revision        - создать миграцию (message=\"название\")"
	@echo "  make db-shell           - psql консоль"
	@echo "  make db-logs            - логи PostgreSQL"
	@echo ""
	@echo "Тестирование:"
	@echo "  make test               - unit тесты"
	@echo "  make test-cov           - тесты с coverage"
	@echo "  make test-integration   - integration тесты"
	@echo "  make test-all           - все тесты"
	@echo ""
	@echo "Качество кода (Backend):"
	@echo "  make format             - форматирование (ruff)"
	@echo "  make lint               - проверка кода (ruff + mypy)"
	@echo "  make check-all          - полная проверка"
	@echo ""
	@echo "Frontend:"
	@echo "  make frontend-install   - установка зависимостей (pnpm)"
	@echo "  make frontend-dev       - dev-сервер (порт 3000)"
	@echo "  make frontend-build     - production сборка"
	@echo "  make frontend-start     - production сервер"
	@echo "  make frontend-lint      - проверка ESLint"
	@echo "  make frontend-format    - форматирование Prettier"
	@echo "  make frontend-type-check - проверка TypeScript"
	@echo "  make frontend-check-all - полная проверка frontend"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build       - сборка всех Docker образов"
	@echo "  make docker-up          - запуск в production режиме"
	@echo "  make docker-dev         - запуск в development режиме"
	@echo "  make docker-down        - остановка всех сервисов"
	@echo "  make docker-logs        - просмотр логов"
	@echo "  make docker-ps          - статус контейнеров"
	@echo "  make docker-restart     - перезапуск сервисов"
	@echo "  make docker-clean       - удаление контейнеров и volumes"
	@echo "  make docker-lint        - проверка Dockerfile (Hadolint)"
	@echo "  make docker-scan        - сканирование безопасности (Trivy)"
	@echo ""
	@echo "CI/CD (локальное воспроизведение):"
	@echo "  make ci-lint-backend    - lint backend как в CI"
	@echo "  make ci-lint-frontend   - lint frontend как в CI"
	@echo "  make ci-test            - тесты как в CI"
	@echo "  make ci-build           - сборка образов как в CI"
	@echo "  make ci-check-all       - полная CI проверка локально"
	@echo ""
	@echo "Утилиты:"
	@echo "  make clean              - очистка временных файлов"
	@echo ""

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

# API Server commands
api-run:
	uv run python -m src.api.server

api-docs:
	@echo "API Documentation:"
	@echo "  OpenAPI/Swagger UI: http://localhost:8000/docs"
	@echo "  ReDoc: http://localhost:8000/redoc"
	@echo ""
	@echo "API Endpoints:"
	@echo "  Root: http://localhost:8000/"
	@echo "  Stats (7d): http://localhost:8000/api/stats?period=7d"
	@echo "  Stats (30d): http://localhost:8000/api/stats?period=30d"
	@echo "  Health: http://localhost:8000/health"

api-test:
	@echo "Testing API endpoint (7 days)..."
	@curl -s http://localhost:8000/api/stats?period=7d | jq
	@echo ""
	@echo "Testing API endpoint (30 days)..."
	@curl -s http://localhost:8000/api/stats?period=30d | jq

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

# Frontend commands (with NVM)
frontend-install:
	cd frontend && $(WITH_NVM) pnpm install

frontend-dev:
	cd frontend && $(WITH_NVM) pnpm dev

frontend-build:
	cd frontend && $(WITH_NVM) pnpm build

frontend-start:
	cd frontend && $(WITH_NVM) pnpm start

frontend-lint:
	cd frontend && $(WITH_NVM) pnpm lint

frontend-format:
	cd frontend && $(WITH_NVM) pnpm format

frontend-type-check:
	cd frontend && $(WITH_NVM) pnpm type-check

frontend-check-all: frontend-lint frontend-type-check

# Docker commands
DOCKER_COMPOSE := docker compose -f devops/docker-compose.yml
DOCKER_COMPOSE_DEV := docker compose -f devops/docker-compose.yml -f devops/docker-compose.dev.yml

docker-build:
	$(DOCKER_COMPOSE) build

docker-up:
	$(DOCKER_COMPOSE) up -d

docker-dev:
	$(DOCKER_COMPOSE_DEV) up

docker-down:
	$(DOCKER_COMPOSE) down

docker-logs:
	$(DOCKER_COMPOSE) logs -f

docker-ps:
	$(DOCKER_COMPOSE) ps

docker-restart:
	$(DOCKER_COMPOSE) restart

docker-clean:
	$(DOCKER_COMPOSE) down -v --rmi local
	@echo "Docker очищен: контейнеры, volumes и локальные образы удалены"

docker-lint:
	@echo "Проверка Dockerfile с помощью Hadolint..."
	@docker run --rm -i hadolint/hadolint < devops/Dockerfile.bot || true
	@docker run --rm -i hadolint/hadolint < devops/Dockerfile.api || true
	@docker run --rm -i hadolint/hadolint < devops/Dockerfile.frontend || true
	@echo "Hadolint проверка завершена"

docker-scan:
	@echo "Сканирование образов с помощью Trivy..."
	@echo "Сканирование systech-aidd-bot..."
	@docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image systech-aidd-live-bot:latest || true
	@echo ""
	@echo "Сканирование systech-aidd-api..."
	@docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image systech-aidd-live-api:latest || true
	@echo ""
	@echo "Сканирование systech-aidd-frontend..."
	@docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image systech-aidd-live-frontend:latest || true
	@echo ""
	@echo "Trivy сканирование завершено"

# CI/CD local reproduction commands
ci-lint-backend:
	@echo "==> Running backend lint (как в CI)..."
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/
	uv run mypy src/ tests/
	@echo "✅ Backend lint passed"

ci-lint-frontend:
	@echo "==> Running frontend lint (как в CI)..."
	cd frontend && $(WITH_NVM) pnpm lint
	cd frontend && $(WITH_NVM) pnpm type-check
	cd frontend && $(WITH_NVM) pnpm format:check
	@echo "✅ Frontend lint passed"

ci-test:
	@echo "==> Running tests (как в CI)..."
	uv run pytest -m "not integration" --cov=src --cov-report=term
	@echo "✅ Tests passed"

ci-build:
	@echo "==> Building Docker images (как в CI)..."
	@echo "Building bot image..."
	docker build -f devops/Dockerfile.bot -t systech-aidd-bot:local .
	@echo "Building api image..."
	docker build -f devops/Dockerfile.api -t systech-aidd-api:local .
	@echo "Building frontend image..."
	docker build -f devops/Dockerfile.frontend -t systech-aidd-frontend:local .
	@echo "✅ All images built successfully"
	@echo ""
	@echo "Built images:"
	@docker images | grep systech-aidd

ci-check-all:
	@echo "========================================"
	@echo "🚀 Running full CI check locally"
	@echo "========================================"
	@echo ""
	$(MAKE) ci-lint-backend
	@echo ""
	$(MAKE) ci-lint-frontend
	@echo ""
	$(MAKE) ci-test
	@echo ""
	$(MAKE) ci-build
	@echo ""
	@echo "========================================"
	@echo "✅ All CI checks passed!"
	@echo "========================================"
