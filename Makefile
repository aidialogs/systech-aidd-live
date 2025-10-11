.PHONY: install run test test-cov format lint check-all clean

install:
	uv sync --extra dev

run:
	uv run python -m src.main

test:
	. .venv/bin/activate && python -m pytest

test-cov:
	uv run pytest

format:
	uv run ruff format src/ tests/

lint:
	uv run ruff check src/ tests/
	uv run mypy src/ tests/

check-all: format lint test-cov

clean:
	rm -rf logs/*.log htmlcov/ .coverage


