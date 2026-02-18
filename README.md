# Simple GeoNames API

Geographic REST API based on [GeoNames](https://www.geonames.org/) data.

## 🚀 Quick Setup

### 1. Prerequisites
- Python 3.10+
- Docker Engine (for PostgreSQL)
- Git

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/jomosen/geonames-api.git
cd geonames-api

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# source .venv/bin/activate   # Linux/Mac

# Install the project in editable mode
pip install -e .
```

### 3. Configure Environment Variables

Copy the example file and adjust as needed:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

The `.env` file should contain:

```env
# Database Configuration
DATABASE_URL=postgresql://app:app@localhost:5432/appdb

# Logging Configuration
LOG_LEVEL=INFO

# File Import Configuration
TEMP_PATH=./tmp
```

### 4. Start PostgreSQL

```bash
# Start the PostgreSQL container
docker-compose up -d postgres

# Verify it's running
docker ps
```

### 5. Verify Configuration

```bash
# Run the verification script
python check_env.py
```

## 📦 Usage

### Import GeoNames Data

```bash
geonames geonames import
```

### Start the API Server

```bash
geonames api start --host 127.0.0.1 --port 8080
```

Or use the CLI with Python module:

```bash
python -m geonames.presentation.cli.main api start
```

Once running, access the interactive API documentation at:
- **Swagger UI**: http://127.0.0.1:8080/docs
- **ReDoc**: http://127.0.0.1:8080/redoc

## 🔧 Development

### Project Structure

```
src/
├── geonames/           # Main application module
│   ├── application/    # Use cases and services
│   ├── domain/         # Entities and business logic
│   ├── infrastructure/ # Implementations (DB, importers)
│   └── presentation/   # REST API and CLI
└── shared/             # Shared utilities (logger, file downloader, database connectors)
```

**Note**: The `shared/` module contains reusable components like logging, file downloading, and database connection utilities. While currently serving only the `geonames` bounded context, this structure allows for easy addition of new bounded contexts in the future without code duplication.

### Architecture

This project follows **Clean Architecture** principles with **Hexagonal Architecture** patterns:
- **Domain Layer**: Business entities and rules (Country, GeoName, AlternateName)
- **Application Layer**: Use cases, services, and port definitions
- **Infrastructure Layer**: Adapters for external systems (PostgreSQL, file importers)
- **Presentation Layer**: Entry points (FastAPI REST endpoints, Typer CLI)

### Environment Variables

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `DATABASE_URL` | PostgreSQL connection URL | - | ✅ |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | INFO | ❌ |
| `TEMP_PATH` | Temporary directory for downloaded files | ./tmp | ❌ |

### Useful Commands

```bash
# Check dependencies
pip check

# View PostgreSQL logs
docker logs -f postgres

# Connect to PostgreSQL with psql
docker exec -it postgres psql -U app -d appdb

# Stop services
docker-compose down

# Stop and remove all data (including database volume)
docker-compose down -v

# Run tests (when available)
pytest

# Format code (when dev dependencies installed)
black src/
ruff check src/
```

## �️ Database Schema

The application uses PostgreSQL with SQLAlchemy ORM. Main entities:
- **Countries**: Country information with ISO codes
- **GeoNames**: Geographic locations (cities, administrative divisions)
- **Alternate Names**: Alternative names for locations in different languages

## 📝 License

MIT - See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This project uses data from [GeoNames](https://www.geonames.org/), which is licensed under a [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/).
