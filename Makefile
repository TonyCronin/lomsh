.PHONY: install dev test live run clean

install:
	pip install .

dev:
	pip install -e ".[dev]"

test:
	python -m pytest tests/ -v

live:
	python -m pytest tests/ -v --live

run:
	lomsh

clean:
	rm -rf build dist *.egg-info __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
