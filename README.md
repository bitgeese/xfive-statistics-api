# XFive Data Statistics API

A Django-based application for importing demographic data from CSV files and providing a REST API for data analysis and visualization.

## Project Overview

This project processes CSV data containing demographic information about non-EU/EFTA/EU candidate citizens in Ireland. It provides:

- Data models to efficiently store demographic statistics
- CSV import functionality with validation and logging
- REST API with filtering and aggregation capabilities
- (Optional) Frontend data visualization

## Technologies

- Python 3.12+
- Django 5.1
- Django REST Framework
- Poetry for dependency management
- Pandas for data processing
- Ruff for code linting and formatting

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Poetry for dependency management

### Installation

1. Clone the repository:
   ```
   git clone [repository-url]
   cd xfive
   ```

2. Install dependencies with Poetry:
   ```
   poetry install
   ```
   
   or use the Makefile:
   ```
   make install
   ```

3. Run database migrations:
   ```
   python manage.py migrate
   ```
   
   or use the Makefile:
   ```
   make migrate
   ```

4. Create a superuser (optional but recommended):
   ```
   make create-superuser
   ```

5. Start the development server:
   ```
   python manage.py runserver
   ```
   
   or use the Makefile:
   ```
   make dev-server
   ```

## Data Import

The application can import demographic data from CSV files:

```
python manage.py import_csv [path-to-csv-file]
```

or use the Makefile:

```
make import-data CSV=path/to/data.csv
```

The import process will:
- Validate CSV data structure
- Skip invalid or incomplete entries
- Log import statistics and issues
- Store data in appropriate models, avoiding duplication

## API Documentation

The API provides several endpoints for accessing and filtering demographic data:

### API Endpoints

- `GET /api/demographics/` - List all demographic statistics with optional filtering
  - Query parameters: `year`, `age_group`, `sex`, `hd_index`
  - Returns aggregated statistics including both male and female counts

### Swagger Documentation

API documentation is available via Swagger UI:

```
/api/swagger/
```

## Development

### Available Make Commands

This project includes a Makefile with useful commands:

- `make help` - Display available commands
- `make setup` - Initial project setup (install deps + migrate)
- `make install` - Install dependencies with Poetry
- `make migrate` - Run database migrations
- `make dev-server` - Run development server
- `make lint` - Check code with Ruff
- `make format` - Format code with Ruff
- `make test` - Run tests
- `make test-cov` - Run tests with coverage
- `make clean` - Remove Python cache files
- `make import-data CSV=file.csv` - Import CSV data
- `make create-superuser` - Create a Django superuser

### Running Tests

```
make test
```

For test coverage:

```
make test-cov
```

### Code Quality

This project uses Ruff for linting and code formatting:

```
make lint     # Check code quality
make format   # Format code
```

## Project Structure

```
xfive/                     # Main project directory
├── data_statistics/       # Project configuration
├── demographics/          # Main app for demographic data
│   ├── models.py          # Data models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API endpoints
│   ├── management/        # Custom management commands
│   │   └── commands/      # Contains import_csv command
├── data/                  # Storage for CSV files
├── tests/                 # Project tests
├── Makefile               # Common development commands
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## Deliverables

- Django models for demographic data
- CSV import functionality
- REST API with filtering and aggregation
- Documentation for setup and usage
