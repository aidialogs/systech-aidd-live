.PHONY: install run test clean

install:
	uv sync --extra dev

run:
	uv run python -m src.main

test:
	. .venv/bin/activate && python -m pytest

clean:
	rm -rf logs/*.log


