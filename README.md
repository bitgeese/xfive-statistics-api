# XFive Data Statistics API

A Django-based application for importing demographic data from CSV files and providing a REST API for data analysis and visualization.

## Project Overview

This project processes CSV data containing demographic information about non-EU/EFTA/EU candidate citizens in Ireland. It provides:

- Data models to efficiently store demographic statistics
- CSV import functionality with validation and logging
- REST API with filtering and aggregation capabilities
- (Optional) Frontend data visualization

## Features and Implementation

### Data Models

The application uses a normalized database structure to avoid duplication of data:

- **AgeGroup**: Stores age categories like "0 - 4 years", "5 - 9 years", etc.
- **Sex**: Stores gender categories ("Male", "Female")
- **HDIndex**: Stores Human Development Index categories (High, Medium, Low, Very High)
- **DemographicStatistic**: Stores the actual statistics with references to the categories

The models follow a "fat models, thin views" approach with business logic implemented at the model level for aggregating and filtering data.

### CSV Import

The application provides two ways to import data:

1. **From file**: Import from a local CSV file
2. **From URL**: Import directly from a URL (like the CSO Ireland data portal)

The import process:
- Validates CSV data structure
- Skips aggregated data (e.g., "All ages", "Both sexes") to avoid duplication
- Maps codes to meaningful names (e.g., "1" → "Male", "2" → "Female")
- Handles errors gracefully with detailed logging
- Stores only unique combinations of data

### Query and Aggregation

The data models provide methods to dynamically calculate aggregated statistics:

- Get total statistics for both sexes
- Get statistics aggregated by all age groups
- Get statistics aggregated across all HDI categories
- Filter statistics by various combinations of criteria

### Development Approach

This project was developed using Test-Driven Development (TDD):

1. **Write Tests First**: All features began with test cases defining expected behavior
2. **Implement Features**: Code was written to pass the tests
3. **Refactor**: Code was improved while maintaining test coverage
4. **Automate Testing**: Comprehensive test suite verifies all functionality

Test coverage includes:
- Unit tests for all models and their methods
- Integration tests for the CSV import process
- Command-line interface tests

## Technologies

- Python 3.12+
- Django 5.1
- Django REST Framework
- Poetry for dependency management
- Python's built-in CSV module for data processing
- httpx for URL-based imports
- pytest for comprehensive testing
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

The application can import demographic data from CSV files or URLs:

### File Import

```
poetry run python manage.py import_demographics --file=path/to/data.csv
```

Or using the Makefile:

```
make import-data CSV=path/to/data.csv
```

### URL Import

```
poetry run python manage.py import_demographics --url=https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/PEA27/CSV/1.0/en
```

Or using the Makefile:

```
make import-url URL=https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/PEA27/CSV/1.0/en
```

The import process outputs:
- Total rows processed
- Number of skipped rows (aggregated data)
- Number of successfully imported rows
- Any errors encountered

### Viewing Imported Data

To see a summary of the imported data and some sample records:

```
poetry run python manage.py show_statistics
```

Or using the Makefile:

```
make show-stats
```

You can filter by year and limit the number of records shown:

```
poetry run python manage.py show_statistics --year=2023 --limit=20
```

Or using the Makefile:

```
make show-stats YEAR=2023 LIMIT=20
```

This command shows:
- Counts of different categories
- Years available in the database
- Sample records
- Example of aggregated statistics

## API Usage

The API provides several endpoints for accessing and filtering demographic data:

### API Endpoints

- `GET /api/demographics/` - List all demographic statistics with optional filtering
  - Query parameters: `year`, `age_group`, `sex`, `hd_index`
  - Returns aggregated statistics including both male and female counts

### Example Queries

Filtering by age group and HDI category:
```
GET /api/demographics/?age_group=20 - 24 years&hd_index=High Human Development Index (HDI)
```

The response includes both the individual statistics and the aggregated total for both sexes.

## Development

### Running Tests

The project includes comprehensive tests for all components:

```
poetry run python -m pytest
```

For testing specific components:

```
poetry run python -m pytest tests/test_models.py
poetry run python -m pytest tests/test_csv_import.py
```

### Code Quality

This project uses Ruff for linting and code formatting:

```
make lint     # Check code quality
make format   # Format code
```

## Contributing

Contributions to this project are welcome! Here's how you can help:

1. **Report Issues**: If you find a bug or have a feature request, please open an issue.
2. **Contribute Code**: Follow these steps to contribute code:
   - Fork the repository
   - Create a feature branch (`git checkout -b feature/amazing-feature`)
   - Write tests for your feature
   - Implement your feature
   - Ensure all tests pass
   - Commit your changes (`git commit -m 'Add amazing feature'`)
   - Push to the branch (`git push origin feature/amazing-feature`)
   - Open a Pull Request

### Development Guidelines

When contributing, please follow these guidelines:

- Write tests for all new features
- Follow the existing code style and structure
- Add appropriate documentation
- Keep commits small and focused
- Write clear commit messages

## Project Structure

```
xfive/                     # Main project directory
├── data_statistics/       # Project configuration
├── demographics/          # Main app for demographic data
│   ├── models.py          # Data models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API endpoints
│   ├── importers.py       # CSV import functionality
│   ├── management/        # Custom management commands
│   │   └── commands/      # Contains import_demographics command
├── data/                  # Storage for CSV files
├── tests/                 # Project tests
│   ├── conftest.py        # pytest configuration
│   ├── test_models.py     # Model tests
│   ├── test_model_methods.py # Model method tests
│   ├── test_csv_import.py # CSV import tests
│   ├── fixtures/          # Test fixtures
├── Makefile               # Common development commands
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## Implementation Details

### Model Features

- **BaseCategory**: Abstract base model for all category models
- **Validation**: Input validation to ensure data integrity
- **Indexing**: Database indexes for optimal query performance
- **Aggregation Methods**: Methods to compute totals for various dimensions
- **Type Hints**: Comprehensive type hints for better IDE support and code quality

### CSV Importer Features

- **CSV to Model Mapping**: Intelligent mapping of CSV fields to model fields
- **Code Translation**: Handling of coded values (e.g., "1" for Male)
- **Atomic Transactions**: All-or-nothing imports to prevent partial data
- **Duplicate Handling**: Update-or-create logic to handle repeated imports
- **URL Support**: Direct import from CSO data portal URL

### Error Handling

- **Validation Errors**: Detailed logging of data validation issues
- **Import Statistics**: Comprehensive reporting of import results
- **Transactional Safety**: Database integrity protection through transactions

## Next Steps

Future enhancements for this project may include:

- Frontend data visualization with interactive charts
- Additional data sources integration
- Export functionality to various formats (CSV, Excel, JSON)
- Advanced analytics and statistical calculations
- Caching for improved performance with large datasets

## Deliverables

- Django models for demographic data
- CSV import functionality
- REST API with filtering and aggregation
- Documentation for setup and usage
