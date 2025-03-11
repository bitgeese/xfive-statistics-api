.PHONY: help setup install migrate dev-server test test-cov test-cov-html lint format import-data import-url show-stats clean create-superuser docker-build docker-up docker-down docker-exec docker-test docker-prod-build docker-prod-up docker-prod-down docker-setup docker-prod-setup

PYTHON = poetry run python
MANAGE = $(PYTHON) manage.py

help:
	@echo "Available commands:"
	@echo "  make setup           - Interactive setup wizard (recommended)"
	@echo "  make install         - Install dependencies with Poetry"
	@echo "  make migrate         - Run database migrations"
	@echo "  make dev-server      - Run development server"
	@echo "  make test            - Run tests"
	@echo "  make test-cov        - Run tests with coverage report in console"
	@echo "  make test-cov-html   - Run tests with HTML coverage report"
	@echo "  make lint            - Check code with Ruff"
	@echo "  make format          - Format code with Ruff"
	@echo "  make import-data     - Import CSV data from file (specify CSV=path/to/file.csv)"
	@echo "  make import-url      - Import CSV data from URL (specify URL=https://example.com/data.csv)"
	@echo "  make show-stats      - Show statistics about imported data (optional: YEAR=2023 LIMIT=10)"
	@echo "  make clean           - Remove Python cache files"
	@echo "  make create-superuser - Create a Django superuser"
	@echo "  make docker-setup    - Set up Docker development environment (recommended)"
	@echo "  make docker-build    - Build Docker containers for development"
	@echo "  make docker-up       - Start Docker containers for development"
	@echo "  make docker-down     - Stop Docker containers for development"
	@echo "  make docker-exec     - Execute command in Docker container (specify CMD='command')"
	@echo "  make docker-test     - Run tests in Docker container"
	@echo "  make docker-prod-setup - Set up Docker production environment"
	@echo "  make docker-prod-build - Build Docker containers for production"
	@echo "  make docker-prod-up  - Start Docker containers for production"
	@echo "  make docker-prod-down - Stop Docker containers for production"

setup:
	@echo "Running setup wizard..."
	@chmod +x setup.sh
	./setup.sh

install:
	@echo "Installing dependencies..."
	poetry install --no-root

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

test-cov:
	@echo "Running tests with coverage..."
	poetry run pytest --cov=demographics --cov=visualization --cov-report=term

test-cov-html:
	@echo "Running tests with HTML coverage report..."
	poetry run pytest --cov=demographics --cov=visualization --cov-report=html
	@echo "HTML coverage report generated in htmlcov/ directory"

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

# Docker commands
docker-setup:
	@echo "Setting up Docker development environment..."
	@chmod +x scripts/docker-setup.sh
	./scripts/docker-setup.sh

docker-build:
	@echo "Building Docker containers..."
	docker compose build

docker-up:
	@echo "Starting Docker containers..."
	docker compose up -d

docker-down:
	@echo "Stopping Docker containers..."
	docker compose down

docker-exec:
	@if [ -z "$(CMD)" ]; then \
		echo "Error: Command not specified. Use CMD='command'"; \
		exit 1; \
	fi
	@echo "Executing command in Docker container: $(CMD)"
	docker compose exec web $(CMD)

docker-test:
	@echo "Running tests in Docker container..."
	docker compose exec web pytest

# Docker production commands
docker-prod-setup:
	@echo "Setting up Docker production environment..."
	@if [ ! -f .env.prod ]; then \
		echo "Warning: .env.prod file not found. Creating from .env.prod.example..."; \
		cp .env.prod.example .env.prod; \
		echo "Please edit .env.prod with your production settings before continuing."; \
		exit 1; \
	fi
	docker compose -f docker-compose.prod.yml build
	docker compose -f docker-compose.prod.yml up -d

docker-prod-build:
	@echo "Building Docker production containers..."
	docker compose -f docker-compose.prod.yml build

docker-prod-up:
	@echo "Starting Docker production containers..."
	docker compose -f docker-compose.prod.yml up -d

docker-prod-down:
	@echo "Stopping Docker production containers..."
	docker compose -f docker-compose.prod.yml down

# Ensure data directory exists
data:
	mkdir -p data

.PHONY: data 