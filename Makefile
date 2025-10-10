.PHONY: install run test clean

install:
	uv sync

run:
	uv run python -m src.main

test:
	uv run pytest

clean:
	rm -rf logs/*.log


