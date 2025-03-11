#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================${NC}"
echo -e "${BLUE}XFive Data Statistics API Setup Tool${NC}"
echo -e "${BLUE}====================================${NC}"
echo

# Check if we're in the right directory by looking for key files
if [ ! -f "pyproject.toml" ] || [ ! -f "manage.py" ]; then
    echo -e "${RED}[✗] Error: This doesn't appear to be the project root directory.${NC}"
    echo -e "${YELLOW}Please run this script from the root of the XFive project.${NC}"
    exit 1
fi

# Create README.md if it doesn't exist
if [ ! -f "README.md" ]; then
    echo -e "${YELLOW}[!] README.md not found. Creating a simple README...${NC}"
    echo "# XFive Data Statistics API" > README.md
    echo -e "A Django application that processes demographic data from CSV files and provides an API for data analysis with visualization.\n" >> README.md
    echo -e "See the documentation for more details.\n" >> README.md
fi

# Check for Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}[✓] Python installed:${NC} $PYTHON_VERSION"
else
    echo -e "${RED}[✗] Python 3 not found. Please install Python 3.12 or higher.${NC}"
    exit 1
fi

# Check for Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo -e "${GREEN}[✓] Docker installed:${NC} $DOCKER_VERSION"
    
    if command -v docker compose &> /dev/null; then
        COMPOSE_VERSION=$(docker compose version)
        echo -e "${GREEN}[✓] Docker Compose installed:${NC} $COMPOSE_VERSION"
        DOCKER_AVAILABLE=true
    else
        echo -e "${YELLOW}[!] Docker Compose not found. Docker setup option will not be available.${NC}"
        DOCKER_AVAILABLE=false
    fi
else
    echo -e "${YELLOW}[!] Docker not found. Docker setup option will not be available.${NC}"
    DOCKER_AVAILABLE=false
fi

# Check for Poetry
if command -v poetry &> /dev/null; then
    POETRY_VERSION=$(poetry --version)
    echo -e "${GREEN}[✓] Poetry installed:${NC} $POETRY_VERSION"
    POETRY_AVAILABLE=true
else
    echo -e "${YELLOW}[!] Poetry not found. Local setup option will require manual pip installation.${NC}"
    POETRY_AVAILABLE=false
fi

# Ensure necessary directories exist
mkdir -p data
mkdir -p scripts

echo
echo -e "${BLUE}Choose a setup method:${NC}"
echo -e "  1) ${GREEN}Docker setup${NC} (recommended, requires Docker)"
echo -e "  2) ${GREEN}Local Poetry setup${NC} (requires Poetry)"
echo -e "  3) ${GREEN}Local Pip setup${NC} (minimal dependencies)"
echo -e "  4) ${GREEN}Exit${NC}"
echo

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        if [ "$DOCKER_AVAILABLE" = true ]; then
            echo -e "${GREEN}Setting up with Docker...${NC}"
            
            # Ensure directories exist
            mkdir -p data
            
            # Run the Docker setup script
            if [ -f ./scripts/docker-setup.sh ]; then
                chmod +x ./scripts/docker-setup.sh
                ./scripts/docker-setup.sh
            else
                echo -e "${RED}Docker setup script not found.${NC}"
                echo -e "${YELLOW}Running docker-compose directly...${NC}"
                docker compose build && docker compose up -d
            fi
        else
            echo -e "${RED}Docker is not available. Please install Docker and Docker Compose first.${NC}"
            exit 1
        fi
        ;;
    2)
        if [ "$POETRY_AVAILABLE" = true ]; then
            echo -e "${GREEN}Setting up with Poetry...${NC}"
            
            # Install dependencies with Poetry
            poetry install
            
            # Run migrations
            poetry run python manage.py migrate
            
            echo -e "${GREEN}Setup complete!${NC}"
            echo -e "${YELLOW}To start the development server, run:${NC}"
            echo -e "  poetry run python manage.py runserver"
            echo -e "or"
            echo -e "  make dev-server"
        else
            echo -e "${RED}Poetry is not available. Please install Poetry first or choose another option.${NC}"
            exit 1
        fi
        ;;
    3)
        echo -e "${GREEN}Setting up with Pip...${NC}"
        
        # Create and activate virtual environment
        python3 -m venv venv
        
        if [ -f venv/bin/activate ]; then
            source venv/bin/activate
            echo -e "${GREEN}Virtual environment created and activated.${NC}"
            
            # Install requirements
            if [ -f requirements.txt ]; then
                pip install -r requirements.txt
            else
                echo -e "${YELLOW}requirements.txt not found. Creating from pyproject.toml...${NC}"
                # Extract dependencies from pyproject.toml and install
                if [ -f pyproject.toml ]; then
                    pip install -e .
                else
                    echo -e "${RED}Neither requirements.txt nor pyproject.toml found.${NC}"
                    exit 1
                fi
            fi
            
            # Run migrations
            python manage.py migrate
            
            echo -e "${GREEN}Setup complete!${NC}"
            echo -e "${YELLOW}To start the development server, run:${NC}"
            echo -e "  source venv/bin/activate"
            echo -e "  python manage.py runserver"
        else
            echo -e "${RED}Failed to create virtual environment.${NC}"
            exit 1
        fi
        ;;
    4)
        echo -e "${YELLOW}Exiting setup.${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac 