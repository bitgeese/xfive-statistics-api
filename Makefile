.PHONY: help install migrate dev-server test lint format import-data import-url show-stats clean create-superuser

PYTHON = poetry run python
MANAGE = $(PYTHON) manage.py

help:
	@echo "Available commands:"
	@echo "  make install         - Install dependencies with Poetry"
	@echo "  make migrate         - Run database migrations"
	@echo "  make dev-server      - Run development server"
	@echo "  make test            - Run tests"
	@echo "  make lint            - Check code with Ruff"
	@echo "  make format          - Format code with Ruff"
	@echo "  make import-data     - Import CSV data from file (specify CSV=path/to/file.csv)"
	@echo "  make import-url      - Import CSV data from URL (specify URL=https://example.com/data.csv)"
	@echo "  make show-stats      - Show statistics about imported data (optional: YEAR=2023 LIMIT=10)"
	@echo "  make clean           - Remove Python cache files"
	@echo "  make create-superuser - Create a Django superuser"

install:
	@echo "Installing dependencies..."
	poetry install

migrate:
	@echo "Running migrations..."
	$(MANAGE) makemigrations
	$(MANAGE) migrate

dev-server:
	@echo "Starting development server..."
	$(MANAGE) runserver

test:
	@echo "Running tests..."
	poetry run pytest

lint:
	@echo "Linting code..."
	poetry run ruff check .

format:
	@echo "Formatting code..."
	poetry run ruff format .

clean:
	@echo "Cleaning Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

import-data:
	@if [ -z "$(CSV)" ]; then \
		echo "Error: CSV file path not specified. Use CSV=path/to/file.csv"; \
		exit 1; \
	fi
	@echo "Importing data from $(CSV)..."
	$(MANAGE) import_demographics --file=$(CSV)

import-url:
	@if [ -z "$(URL)" ]; then \
		echo "Error: URL not specified. Use URL=https://example.com/data.csv"; \
		exit 1; \
	fi
	@echo "Importing data from URL $(URL)..."
	$(MANAGE) import_demographics --url=$(URL)

show-stats:
	@echo "Showing statistics..."
	@if [ -n "$(YEAR)" ] && [ -n "$(LIMIT)" ]; then \
		$(MANAGE) show_statistics --year=$(YEAR) --limit=$(LIMIT); \
	elif [ -n "$(YEAR)" ]; then \
		$(MANAGE) show_statistics --year=$(YEAR); \
	elif [ -n "$(LIMIT)" ]; then \
		$(MANAGE) show_statistics --limit=$(LIMIT); \
	else \
		$(MANAGE) show_statistics; \
	fi

create-superuser:
	@echo "Creating superuser..."
	$(MANAGE) createsuperuser

# Ensure data directory exists
data:
	mkdir -p data

.PHONY: data 