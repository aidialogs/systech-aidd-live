# Makefile для systech-aidd-live
#
# Команды для разработки:
#   make install            - установка зависимостей (включая dev-инструменты)
#   make run                - запуск бота
#
# Команды для базы данных:
#   make db-up              - запуск PostgreSQL через Docker Compose
#   make db-down            - остановка PostgreSQL
#   make db-migrate         - применение миграций БД
#   make db-rollback        - откат последней миграции
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
.PHONY: install run db-up db-down db-migrate db-rollback test test-cov test-all test-integration format lint check-all clean

install:
	uv sync --extra dev

run:
	uv run python -m src.main

db-up:
	docker compose up -d postgres

db-down:
	docker compose down

db-migrate:
	uv run yoyo apply migrations

db-rollback:
	uv run yoyo rollback migrations

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


