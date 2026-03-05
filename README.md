# Simple GeoNames API

Geographic REST API based on [GeoNames](https://www.geonames.org/) data.

## 🚀 Quick Setup

### 1. Prerequisites
- Python 3.10+
- Docker Engine (for PostgreSQL and Redis)
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

# Redis Cache Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_TTL=3600
```

### 4. Start Services

```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Verify they are running
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

## 🌐 API Endpoints

### Countries

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/countries` | List countries with optional filters |

**Filters**: `iso_alpha2`, `continent`, `min_population`, `max_population`, `currency_code`

### Administrative Divisions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/countries/{country_code}/admin-divisions` | List administrative divisions |

**Filters**: `feature_code`, `admin1_code`, `limit` (default 100, max 10000), `offset`, `expand`

### Cities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/countries/{country_code}/cities` | List cities with optional filters |
| GET | `/countries/{country_code}/cities/avg-population` | Average population of filtered cities |

**Filters**: `admin1_code`, `admin2_code`, `min_population`, `language`, `limit` (default 100, max 10000), `offset`, `expand`

#### Expand parameter

The `expand` query parameter adds related data via JOINs. Pass values as comma-separated:

| Value | Description |
|-------|-------------|
| `country_name` | Full country name |
| `postal_code_regex` | Country postal code regex |
| `admin1_name` | Name of the first-level administrative division |

```
GET /countries/ES/cities?expand=country_name,admin1_name
```

### Cache Header

All responses include an `X-Cache` header indicating the data source:

```
X-Cache: HIT   → served from Redis cache
X-Cache: MISS  → queried from PostgreSQL (and cached for next time)
```

## 🔧 Development

### Project Structure

```
src/
├── geonames/           # Main application module
│   ├── application/    # Use cases, services, DTOs, and ports
│   ├── domain/         # Entities and business logic
│   ├── infrastructure/ # Implementations (DB, Redis cache, importers)
│   └── presentation/   # REST API and CLI
└── shared/             # Shared utilities (logger, file downloader, database/cache connectors)
```

**Note**: The `shared/` module contains reusable components like logging, file downloading, and database/cache connection utilities. While currently serving only the `geonames` bounded context, this structure allows for easy addition of new bounded contexts in the future without code duplication.

### Architecture

This project follows **Clean Architecture** principles with **Hexagonal Architecture** patterns:
- **Domain Layer**: Business entities and rules (Country, GeoName, AlternateName)
- **Application Layer**: Use cases, services, DTOs, and port definitions (including `CachePort`)
- **Infrastructure Layer**: Adapters for external systems (PostgreSQL, Redis, file importers)
- **Presentation Layer**: Entry points (FastAPI REST endpoints, Typer CLI)

Query repositories use a **Decorator pattern** for caching: each ORM repository is wrapped by a cached counterpart (`CachedCityQueryRepository`, etc.) that is transparent to the service layer.

### Environment Variables

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `DATABASE_URL` | PostgreSQL connection URL | - | ✅ |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | INFO | ❌ |
| `TEMP_PATH` | Temporary directory for downloaded files | ./tmp | ❌ |
| `REDIS_URL` | Redis connection URL | redis://localhost:6379/0 | ❌ |
| `REDIS_TTL` | Cache TTL in seconds | 3600 | ❌ |

### Useful Commands

```bash
# Check dependencies
pip check

# View PostgreSQL logs
docker logs -f postgres

# Connect to PostgreSQL with psql
docker exec -it postgres psql -U app -d appdb

# Check Redis is running
docker exec -it redis redis-cli ping

# Monitor Redis cache in real time
docker exec -it redis redis-cli monitor

# Stop services
docker-compose down

# Stop and remove all data (including volumes)
docker-compose down -v

# Run tests (when available)
pytest

# Format code (when dev dependencies installed)
black src/
ruff check src/
```

## 🗄️ Database Schema

The application uses PostgreSQL with SQLAlchemy ORM. Main entities:
- **Countries**: Country information with ISO codes
- **Cities**: City-level geographic locations
- **Admin Divisions**: Administrative divisions (ADM1–ADM4)
- **Alternate Names**: Alternative names for locations in different languages

## 📝 License

MIT - See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This project uses data from [GeoNames](https://www.geonames.org/), which is licensed under a [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/).
