# Makefile для systech-aidd-live
#
# Команды для начальной настройки:
#   make venv               - создание виртуального окружения (uv venv)
#
# Команды для разработки Backend:
#   make install            - установка зависимостей (включая dev-инструменты)
#   make run                - запуск только бота
#   make run-api            - запуск только API сервера
#   make run-combined       - запуск бота и API вместе (рекомендуется)
#   make api-check          - проверка API endpoints
#
# Команды для разработки Frontend (Dashboard):
#   make dashboard-install  - установка зависимостей dashboard (pnpm install)
#   make dashboard-dev      - запуск dev сервера (http://localhost:3000)
#   make dashboard-build    - production сборка
#   make dashboard-start    - запуск production сервера
#   make dashboard-lint     - ESLint проверка
#   make dashboard-type-check - TypeScript проверка типов
#   make dashboard-check    - полная проверка (type-check + lint + build)
#   make dashboard-clean    - очистка .next, node_modules
#
# Комбинированные команды (Backend + Frontend):
#   make dev-all            - запуск API + Dashboard одновременно
#
# Команды для тестирования Backend:
#   make test               - запуск unit тестов (без integration)
#   make test-cov           - запуск тестов с coverage (без integration)
#   make test-integration   - запуск только integration тестов (реальные API вызовы)
#   make test-all           - запуск всех тестов (unit + integration)
#
# Команды для качества кода Backend:
#   make format             - автоформатирование кода (ruff format)
#   make lint               - проверка кода (ruff check + mypy)
#   make check-all          - полная проверка (format + lint + test-cov)
#
# Утилиты:
#   make clean              - очистка логов и временных файлов
#
.PHONY: venv install run run-api run-combined api-check test test-cov test-all test-integration format lint check-all clean
.PHONY: dashboard-install dashboard-dev dashboard-build dashboard-start dashboard-lint dashboard-type-check dashboard-check dashboard-clean dev-all

venv:
	@echo "📦 Creating virtual environment with uv..."
	uv venv
	@echo ""
	@echo "✅ Virtual environment created at .venv/"
	@echo ""
	@echo "To activate it, run:"
	@echo "  source .venv/bin/activate"
	@echo ""
	@echo "Then install dependencies with:"
	@echo "  make install"

install:
	uv sync --extra dev

run:
	uv run python -m src.main

run-api:
	uv run python -m src.api_main

run-combined:
	uv run python -m src.combined_main

api-check:
	@echo "🔍 Checking API endpoints..."
	@echo ""
	@echo "1. Health check:"
	@curl -s http://localhost:8000/health | python -m json.tool
	@echo ""
	@echo "2. Stats (default 7d):"
	@curl -s http://localhost:8000/api/stats | python -m json.tool
	@echo ""
	@echo "3. Stats (30d):"
	@curl -s "http://localhost:8000/api/stats?time_range=30d" | python -m json.tool
	@echo ""
	@echo "✅ API check complete. Open http://localhost:8000/docs for Swagger UI"

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

# ============================================
# Frontend (Dashboard) Commands
# ============================================

dashboard-install:
	@echo "📦 Installing dashboard dependencies..."
	cd dashboard && pnpm install
	@echo "✅ Dashboard dependencies installed"

dashboard-dev:
	@echo "🚀 Starting dashboard dev server..."
	@echo "🌐 Dashboard will be available at http://localhost:3000"
	@echo "🔗 Make sure API is running at http://localhost:8000"
	@echo ""
	cd dashboard && pnpm dev

dashboard-build:
	@echo "🏗️  Building dashboard for production..."
	cd dashboard && pnpm build
	@echo "✅ Dashboard build complete"

dashboard-start:
	@echo "🚀 Starting dashboard production server..."
	@echo "🌐 Dashboard available at http://localhost:3000"
	cd dashboard && pnpm start

dashboard-lint:
	@echo "🔍 Linting dashboard..."
	cd dashboard && pnpm lint
	@echo "✅ Dashboard lint complete"

dashboard-type-check:
	@echo "🔍 Type-checking dashboard..."
	cd dashboard && pnpm type-check
	@echo "✅ Dashboard type-check complete"

dashboard-check: dashboard-type-check dashboard-lint dashboard-build
	@echo ""
	@echo "✅ All dashboard checks passed!"

dashboard-clean:
	@echo "🧹 Cleaning dashboard..."
	rm -rf dashboard/.next dashboard/node_modules dashboard/.turbo
	@echo "✅ Dashboard cleaned"

# ============================================
# Combined Commands (Backend + Frontend)
# ============================================

dev-all:
	@echo "🚀 Starting Backend API + Frontend Dashboard..."
	@echo ""
	@echo "🔧 Backend API will be at http://localhost:8000"
	@echo "🌐 Frontend Dashboard will be at http://localhost:3000"
	@echo ""
	@echo "Press Ctrl+C to stop all services"
	@echo ""
	@trap 'kill 0' INT; \
	make run-api & \
	make dashboard-dev & \
	wait


