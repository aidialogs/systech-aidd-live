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
#
.PHONY: install run test test-cov test-all test-integration format lint check-all clean
.PHONY: db-up db-down db-migrate db-rollback db-revision db-shell db-logs

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
