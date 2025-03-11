$ XFive Data Statistics API

A Django application that processes demographic data from CSV files and provides an API for data analysis with visualization.

## Project Overview

This application processes demographic data for non-EU/EFTA/EU candidate citizens in Ireland, providing:

- Normalized data models to avoid duplication
- CSV import functionality with validation
- REST API with filtering and aggregation
- Data visualization dashboard

## Features

### Data Models

- **AgeGroup**: Age categories (e.g., "0 - 4 years")
- **Sex**: Gender categories (Male, Female)
- **HDIndex**: Human Development Index categories
- **DemographicStatistic**: Statistics with foreign keys to categories

The models are designed to avoid storing aggregate values directly. Aggregates are calculated dynamically when needed.

### CSV Import

Two import methods are supported:
- From local CSV file
- From URL

The import process:
- Validates data and skips aggregated rows
- Maps codes to meaningful names
- Reports success/failure statistics

### API

Filtering capabilities:
- Filter by year, age group, sex, HDI category
- Returns aggregated statistics for both sexes

### Dashboard

- Interactive charts for demographic visualization
- Data filtering options
- CSV import functionality
- Data table with pagination

## Getting Started

### Prerequisites

- Python 3.12+
- Docker and Docker Compose (for container-based setup, recommended)
- Poetry (for local development with Poetry)

### Quick Setup (Recommended)

Use the interactive setup script to choose your preferred installation method:

```bash
./setup.sh
```

This will guide you through the setup process and detect available tools on your system.

### Installation Options

#### Option 1: Docker Compose Setup (Recommended)

The simplest way to get started is using the Docker setup:

```bash
make docker-setup
```

This will:
1. Check for Docker and Docker Compose
2. Create a `.env` file if needed
3. Build and start the containers
4. Provide feedback and next steps

After setup, the application will be available at: http://localhost:8000

#### Option 2: Local Poetry Setup

1. Clone the repository:
   ```
   git clone https://github.com/bitgeese/xfive-statistics-api
   cd xfive-statistics-api
   ```

2. Install dependencies:
   ```
   make install
   ```
   or
   ```
   poetry install
   ```

3. Run migrations:
   ```
   make migrate
   ```

4. Start the development server:
   ```
   make dev-server
   ```

#### Option 3: Local Pip Setup

1. Clone the repository:
   ```
   git clone https://github.com/bitgeese/xfive-statistics-api
   cd xfive-statistics-api
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Start the development server:
   ```
   python manage.py runserver
   ```

For more detailed Docker instructions, see [DOCKER.md](DOCKER.md).

## Data Import

### Import from file:
```
make import-data CSV=path/to/file.csv
```

### Import from URL:
```
make import-url URL=https://example.com/data.csv
```

## API Usage

- `GET /api/demographics/` - List all statistics with filtering options
  - Query parameters: `year`, `age_group`, `sex`, `hd_index`

### Example Query
```
GET /api/demographics/?age_group=20 - 24 years&hd_index=High Human Development Index (HDI)
```

The response includes both individual statistics and the aggregated total for both sexes in the `total_both_sexes` field.

### API Documentation

Browse interactive documentation at:
- `/api/docs/` - Swagger UI
- `/api/redoc/` - ReDoc

## Dashboard

The application includes a visualization dashboard at:
- `/` or `/dashboard/`

Features:
- Interactive charts
- Filtering options
- Data import interface
- Statistics overview

## Development

### Running Tests

Execute the test suite:
```
make test
```

Generate code coverage report in the console:
```
make test-cov
```
This will display coverage statistics for each module directly in your terminal.

Generate code coverage HTML report:
```
make test-cov-html
```
This will generate detailed HTML coverage reports in the `htmlcov` directory.

### Continuous Integration

This project uses GitHub Actions for continuous integration. The workflow:
- Runs on push to main/master and pull requests
- Tests with Python 3.12
- Checks code style with Ruff
- Runs test suite with coverage reporting
- Enforces minimum 80% test coverage

The CI configuration is in `.github/workflows/tests.yml`.

### Code Quality

Check code for style issues and potential problems:
```
make lint
```

Format code automatically:
```
make format
```

## Deployment

For production deployment instructions, see [DOCKER.md](DOCKER.md#production-environment).
