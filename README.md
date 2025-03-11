# XFive Data Statistics API

A Django-based application for importing demographic data from CSV files, providing a REST API for data analysis, and featuring an interactive visualization dashboard with a modern dark theme.

## Project Overview

This project processes CSV data containing demographic information about non-EU/EFTA/EU candidate citizens in Ireland. It provides:

- Data models to efficiently store demographic statistics
- CSV import functionality with validation and logging
- REST API with filtering and aggregation capabilities
- Modern data visualization dashboard with dark theme
- Advanced filtering and data exploration capabilities

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

### Frontend Visualization Dashboard

The application includes a modern visualization dashboard that provides:

- **Dark Theme Interface**: A sophisticated dark red/black color scheme inspired by xfive's branding
- **Interactive Charts**: Demographics breakdown by HDI category and age distribution visualization
- **Advanced Filtering**: Filter data by year, age group, sex, and HDI category
- **Data Table with Pagination**: View and browse through demographic records with pagination controls
- **Real-time Statistics**: View aggregated statistics based on current filter selections

#### Dashboard Technical Implementation

The dashboard is built using:

- **Django Templates**: For server-side rendering with a component-based structure
- **Alpine.js**: For reactive data binding and UI interactions without a heavy framework
- **Chart.js**: For responsive, animated data visualizations
- **Tailwind CSS**: For utility-first styling with custom color palette
- **Axios**: For AJAX requests to the API

#### Design Highlights

- **Responsive Layout**: Adapts to different screen sizes with a grid-based layout
- **Card-based UI**: Information organized in distinct cards with subtle hover effects
- **Custom Color Palette**: Dark theme with xfive-inspired red accents
- **Micro-animations**: Subtle animations for loading states and interactions
- **Accessible UI**: Clear contrast ratios and intuitive navigation

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
- Alpine.js for reactive frontend
- Chart.js for data visualization
- Tailwind CSS for styling
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

#### Basic Listing
```
GET /api/demographics/
```
Returns a paginated list of all demographic statistics.

#### Filtering by Year
```
GET /api/demographics/?year=2023
```
Returns all statistics for the year 2023.

#### Filtering by Age Group
```
GET /api/demographics/?age_group=0 - 4 years
```
Returns all statistics for the "0 - 4 years" age group.

#### Filtering by Sex
```
GET /api/demographics/?sex=Male
```
Returns all statistics for males.

#### Filtering by HDI Category
```
GET /api/demographics/?hd_index=High Human Development Index (HDI)
```
Returns all statistics for the "High Human Development Index (HDI)" category.

#### Combined Filtering
```
GET /api/demographics/?age_group=20 - 24 years&hd_index=High Human Development Index (HDI)
```
Returns statistics for the "20 - 24 years" age group with "High Human Development Index (HDI)".

The response includes both the individual statistics and the aggregated total for both sexes in the `total_both_sexes` field.

### Response Format

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "year": 2023,
      "age_group": "20 - 24 years",
      "sex": "Male",
      "hd_index": "High Human Development Index (HDI)",
      "value": 150,
      "total_both_sexes": 280
    },
    {
      "year": 2023,
      "age_group": "20 - 24 years",
      "sex": "Female",
      "hd_index": "High Human Development Index (HDI)",
      "value": 130,
      "total_both_sexes": 280
    }
  ]
}
```

### Error Handling

The API provides descriptive error messages when invalid parameters are provided:

```json
{
  "error": "Invalid age_group parameter: 'Non-existent Age Group' does not exist. Please provide a valid age group."
}
```

This helps API consumers quickly understand what went wrong and how to fix their request.

### Pagination

The API uses pagination to limit the number of results returned in a single request. By default, 50 items are returned per page. You can navigate through pages using the `next` and `previous` URLs provided in the response.

### API Documentation

The API includes interactive documentation available at:

- `/api/docs/` - Swagger UI interface for exploring and testing the API
- `/api/redoc/` - ReDoc interface for API documentation

These interfaces provide a convenient way to explore the available endpoints, parameters, and response formats.

## Dashboard Usage

The application provides an interactive dashboard for data visualization and exploration at:

- `/` or `/dashboard/` - Main dashboard interface

### Dashboard Features

#### Data Filtering
- Filter by Year: Focus on specific years in the dataset
- Filter by Age Group: View statistics for specific age ranges
- Filter by Sex: Compare data between Male and Female categories
- Filter by HDI Category: Analyze data across different Human Development Index categories
- Reset Filters: Quickly clear all applied filters

#### Data Visualization
- Demographics by HDI Chart: Bar chart showing male/female breakdown by HDI category
- Age Distribution Chart: Line chart visualizing population distribution across age groups
- Statistics Panel: Quick overview of key metrics (total records, gender ratio, etc.)
- Data Table: Paginated display of records matching current filters

#### Data Management
- Import from CSV: Upload local CSV files directly from the dashboard
- Import from URL: Fetch CSV data from a remote URL
- Database Cleaning: Option to reset the database (with confirmation)

### Dashboard Design

The dashboard features a modern dark theme with xfive-inspired styling:
- Dark red/black color scheme with red accent colors
- Distinct card-based UI with subtle gradient headers
- Responsive layout that adapts to different screen sizes
- Interactive elements with hover effects and focus states
- Consistent typography using the Inter font family

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
xfive/                      # Main project directory
├── data_statistics/        # Project configuration
├── demographics/           # Main app for demographic data
│   ├── models.py           # Data models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API endpoints
│   ├── importers.py        # CSV import functionality
│   ├── management/         # Custom management commands
│   │   └── commands/       # Contains import_demographics command
├── visualization/          # Frontend visualization app
│   ├── views.py            # Dashboard views
│   ├── urls.py             # URL routing
│   ├── templates/          # HTML templates
│   │   ├── base.html       # Base template with layout
│   │   └── dashboard.html  # Dashboard implementation
├── data/                   # Storage for CSV files
├── tests/                  # Project tests
│   ├── conftest.py         # pytest configuration
│   ├── test_models.py      # Model tests
│   ├── test_model_methods.py # Model method tests
│   ├── test_csv_import.py  # CSV import tests
│   ├── fixtures/           # Test fixtures
├── Makefile                # Common development commands
├── pyproject.toml          # Project dependencies
└── README.md               # This file
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

### Frontend Implementation

- **Responsive Design**: Mobile-first approach with responsive breakpoints
- **Reactive UI**: Alpine.js for state management and reactive updates
- **Optimized Charts**: Chart.js with optimized configurations for dark mode
- **Accessible Controls**: Keyboard navigable and screen-reader friendly components
- **Performance Optimization**: Minimal dependencies and efficient DOM updates
- **Form Validation**: Client-side validation with clear error messages

### Error Handling

- **Validation Errors**: Detailed logging of data validation issues
- **Import Statistics**: Comprehensive reporting of import results
- **Transactional Safety**: Database integrity protection through transactions
- **User Feedback**: Flash messages and UI indicators for user actions

## Deliverables

- Django models for demographic data
- CSV import functionality
- REST API with filtering and aggregation
- Frontend visualization dashboard
- Comprehensive documentation
