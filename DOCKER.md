# Docker Setup for XFive Data Statistics API

This document provides instructions for setting up and using the Docker environments for the XFive Data Statistics API project.

## Development Environment

### Quick Setup (Recommended)

Run the automated setup script:

```bash
make docker-setup
```

This will:
1. Check for Docker and Docker Compose
2. Create a `.env` file if needed
3. Build and start the containers
4. Provide feedback and next steps

### Manual Setup

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/bitgeese/xfive-statistics-api
   cd xfive-statistics-api
   ```

2. Create an environment file:
   ```bash
   cp .env.example .env
   ```

3. Build the Docker containers:
   ```bash
   make docker-build
   ```

4. Start the containers:
   ```bash
   make docker-up
   ```

5. The application will be available at: http://localhost:8000

### Development Services

The development setup includes:

- **web**: Django application (http://localhost:8000)
- **db**: PostgreSQL database
- **pgadmin**: PostgreSQL admin interface (http://localhost:5050)

To start with development tools (like pgAdmin):
```bash
docker compose --profile dev up
```

## Production Environment

### Setup

1. Prepare the production environment file:
   ```bash
   cp .env.prod.example .env.prod
   ```

2. Edit `.env.prod` with your production settings:
   - Set a secure `SECRET_KEY`
   - Configure `DJANGO_ALLOWED_HOSTS` for your domain
   - Set strong database passwords

3. Run the production setup:
   ```bash
   make docker-prod-setup
   ```

### Production Services

The production setup includes:

- **web**: Django application with Gunicorn
- **db**: PostgreSQL database
- **nginx**: Nginx web server for serving static files and proxying requests

## Common Tasks

### Running Django Management Commands

```bash
make docker-exec CMD="python manage.py <command>"
```

Examples:
```bash
# Create a superuser
make docker-exec CMD="python manage.py createsuperuser"

# Import data from a CSV file
make docker-exec CMD="python manage.py import_demographics --file=data/your_file.csv"

# Show statistics
make docker-exec CMD="python manage.py show_statistics"
```

### Running Tests

```bash
# Run tests in the Docker container
make docker-test

# Run tests with coverage
make docker-exec CMD="pytest --cov=demographics --cov=visualization --cov-report=term"

# Generate HTML coverage report
make docker-exec CMD="pytest --cov=demographics --cov=visualization --cov-report=html"
```

### Accessing PostgreSQL via pgAdmin

1. Start the containers with the dev profile:
   ```bash
   docker compose --profile dev up
   ```

2. Access pgAdmin at http://localhost:5050
   - Email: dev@example.com
   - Password: pgadmin

3. Add a new server in pgAdmin:
   - Name: xfive
   - Host: db
   - Port: 5432
   - Username: postgres
   - Password: postgres

### Viewing Logs

```bash
# View all logs
docker compose logs

# View logs in real-time
docker compose logs -f

# View logs for a specific service
docker compose logs web
```

### Stopping Containers

```bash
# Development environment
make docker-down

# Production environment
make docker-prod-down
```

To remove volumes as well:
```bash
docker compose down -v
# or for production
docker compose -f docker-compose.prod.yml down -v
```

## Troubleshooting

### Database Connection Issues

If the application cannot connect to the database:

1. Check if the database container is running:
   ```bash
   docker compose ps
   ```

2. Check database logs:
   ```bash
   docker compose logs db
   ```

3. Ensure the wait_for_db command is working properly:
   ```bash
   docker compose logs web
   ```

### File Permissions

If you encounter permission issues with files created by Docker:

```bash
# Fix ownership of files created in Docker containers
sudo chown -R $(id -u):$(id -g) .
```

### Docker Images Taking Too Much Space

To clean up unused Docker resources:

```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune
```