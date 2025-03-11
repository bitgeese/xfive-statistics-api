#!/bin/bash

set -e

# Create directories if they don't exist
mkdir -p scripts
mkdir -p data

# Color
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}[INFO]${NC} Setting up Docker environment for XFive Data Statistics API..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Make sure the Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Docker daemon is not running. Please start Docker and try again."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}[WARN]${NC} .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo -e "${GREEN}[INFO]${NC} .env file created successfully."
fi

# Build Docker containers
echo -e "${GREEN}[INFO]${NC} Building Docker containers..."
docker compose build || {
    echo -e "${RED}[ERROR]${NC} Failed to build Docker containers."
    echo -e "${YELLOW}[DEBUG]${NC} Try running: docker compose build --no-cache"
    exit 1
}

# Start the containers
echo -e "${GREEN}[INFO]${NC} Starting Docker containers..."
docker compose up -d || {
    echo -e "${RED}[ERROR]${NC} Failed to start Docker containers."
    echo -e "${YELLOW}[DEBUG]${NC} Try running: docker compose logs"
    exit 1
}

# Check if containers are running
if [ "$(docker compose ps --services --filter "status=running" | wc -l)" -gt 0 ]; then
    echo -e "${GREEN}[SUCCESS]${NC} Docker containers are running."
    echo -e "${GREEN}[INFO]${NC} The application is available at: http://localhost:8000"
    echo -e "${GREEN}[INFO]${NC} To view logs, run: docker compose logs -f"
    echo -e "${GREEN}[INFO]${NC} To stop containers, run: docker compose down"
    echo
    echo -e "${YELLOW}[TIP]${NC} To run commands inside the container, use:"
    echo -e "  docker compose exec web python manage.py <command>"
    echo -e "  Example: docker compose exec web python manage.py createsuperuser"
else
    echo -e "${RED}[ERROR]${NC} Failed to start containers."
    echo -e "${YELLOW}[DEBUG]${NC} Container logs:"
    docker compose logs
    exit 1
fi 