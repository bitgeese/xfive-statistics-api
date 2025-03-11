# XFive Data Statistics API

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
- Poetry for dependency management

### Installation

1. Clone the repository:
   ```
   git clone [repository-url]
   cd xfive
   ```

2. Install dependencies:
   ```
   make install
   ```

3. Run migrations:
   ```
   make migrate
   ```

4. Start the development server:
   ```
   make dev-server
   ```

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
