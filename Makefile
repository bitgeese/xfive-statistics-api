.PHONY: help setup install migrate dev-server lint format test test-cov clean import-data create-superuser

# Set variables
PYTHON = poetry run python
MANAGE = $(PYTHON) manage.py

help:
	@echo "Available commands:"
	@echo "  make setup           - Initial project setup (install deps + migrate)"
	@echo "  make install         - Install dependencies with Poetry"
	@echo "  make migrate         - Run database migrations"
	@echo "  make dev-server      - Run development server"
	@echo "  make lint            - Check code with Ruff"
	@echo "  make format          - Format code with Ruff"
	@echo "  make test            - Run tests"
	@echo "  make test-cov        - Run tests with coverage"
	@echo "  make clean           - Remove Python cache files"
	@echo "  make import-data     - Import CSV data (specify file with CSV=path/to/file.csv)"
	@echo "  make create-superuser - Create a Django superuser"

setup: install migrate

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

lint:
	@echo "Linting code..."
	poetry run ruff check .

format:
	@echo "Formatting code..."
	poetry run ruff format .

test:
	@echo "Running tests..."
	poetry run pytest

test-cov:
	@echo "Running tests with coverage..."
	poetry run pytest --cov=demographics --cov-report=html

clean:
	@echo "Cleaning Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

import-data:
	@if [ -z "$(CSV)" ]; then \
		echo "Error: CSV file path not specified. Use CSV=path/to/file.csv"; \
		exit 1; \
	fi
	@echo "Importing data from $(CSV)..."
	$(MANAGE) import_csv $(CSV)

create-superuser:
	@echo "Creating superuser..."
	$(MANAGE) createsuperuser

# Ensure data directory exists
data:
	mkdir -p data

.PHONY: data 