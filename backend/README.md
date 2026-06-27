# QuantOS

QuantOS is a modular quantitative trading platform built with **FastAPI** and **SQLAlchemy**, designed to support research, strategy development, backtesting, risk analysis, and (eventually) live trading workflows.

## Project Overview

The backend is organized as a **modular monolith**:
- Each domain feature (e.g., factor modeling, alphas, risk metrics, reporting) lives in its own module under `backend/app/modules/<module_name>/`.
- Each module exposes an `APIRouter` in `routes.py`.
- `backend/app/api/router.py` aggregates all module routers under stable URL prefixes.

## Features

- Modular monolith backend (domain modules)
- REST API with FastAPI routers
- Swagger/OpenAPI docs (`/api/docs`)
- Database initialization hook on startup (`database.init_db()`)
- (Planned) expression/strategy evaluation pipelines

## Architecture

### Directory Layout

- `backend/app/main.py`
  - Creates the FastAPI app
  - Adds CORS middleware
  - Calls `database.init_db()`
  - Includes the aggregated API router

- `backend/app/api/router.py`
  - Registers module routers with URL prefixes

- `backend/app/modules/*`
  - `routes.py` — FastAPI endpoints
  - `schemas.py` — Pydantic request/response models
  - `services.py` — business logic
  - `models.py` — SQLAlchemy models (where implemented)

### Mermaid: High-level API Router Flow

```mermaid
flowchart TD
  U[Client] -->|HTTP| F[FastAPI App (app.main)]
  F -->|include_router| R[Aggregated Router (app.api.router)]
  R -->|prefix=/module| M[Module Router (app.modules.<module>.routes)]
  M --> S[Service Layer (services.py)]
  S --> DB[(Database via SQLAlchemy)]
  M -->|response| U
```

## Module Descriptions

Below are the currently registered API modules (as wired in `backend/app/api/router.py`). Each module’s `routes.py` defines its CRUD-style endpoints.

### Users (`/auth`)

- File: `backend/app/modules/users/routes.py`
- Registered in: `backend/app/api/router.py` with prefix `/auth`

Endpoints:
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Factor Engine (`/factor-engine`)

- File: `backend/app/modules/factor_engine/routes.py`
- Registered in: `backend/app/api/router.py` with prefix `/factor-engine`

CRUD (factor exposures):
- `POST /factor-engine/exposures`
- `GET /factor-engine/exposures`
- `GET /factor-engine/exposures/{exposure_id}`
- `PUT /factor-engine/exposures/{exposure_id}`
- `DELETE /factor-engine/exposures/{exposure_id}`

### Alpha Engine (`/alpha-engine`)

- File: `backend/app/modules/alpha_engine/routes.py`
- Registered in: `backend/app/api/router.py` with prefix `/alpha-engine`

CRUD (alphas):
- `POST /alpha-engine/alphas`
- `GET /alpha-engine/alphas`
- `GET /alpha-engine/alphas/{alpha_id}`
- `PUT /alpha-engine/alphas/{alpha_id}`
- `DELETE /alpha-engine/alphas/{alpha_id}`

### Strategy Engine (`/strategy-engine`)

- File: `backend/app/modules/strategy_engine/routes.py`
- Registered in: `backend/app/api/router.py` with prefix `/strategy-engine`

CRUD (strategies):
- `POST /strategy-engine/strategies`
- `GET /strategy-engine/strategies`
- `GET /strategy-engine/strategies/{strategy_id}`
- `PUT /strategy-engine/strategies/{strategy_id}`
- `DELETE /strategy-engine/strategies/{strategy_id}`

### Backtesting Engine (`/backtesting-engine`)

- File: `backend/app/modules/backtesting_engine/routes.py`
- Registered in: `backend/app/api/router.py` with prefix `/backtesting-engine`

CRUD (backtests):
- `POST /backtesting-engine/backtests`
- `GET /backtesting-engine/backtests`
- `GET /backtesting-engine/backtests/{backtest_id}`
- `PUT /backtesting-engine/backtests/{backtest_id}`
- `DELETE /backtesting-engine/backtests/{backtest_id}`

### Portfolio Optimizer (`/portfolio-optimizer`)

- File: `backend/app/modules/portfolio_optimizer/routes.py`
- Registered in: `backend/app/api/router.py` with prefix `/portfolio-optimizer`

CRUD (portfolios):
- `POST /portfolio-optimizer/portfolios`
- `GET /portfolio-optimizer/portfolios`
- `GET /portfolio-optimizer/portfolios/{portfolio_id}`
- `PUT /portfolio-optimizer/portfolios/{portfolio_id}`
- `DELETE /portfolio-optimizer/portfolios/{portfolio_id}`

### Risk Engine (`/risk-engine`)

- File: `backend/app/modules/risk_engine/routes.py`
- Registered in: `backend/app/api/router.py` with prefix `/risk-engine`

CRUD (risk metrics):
- `POST /risk-engine/risk-metrics`
- `GET /risk-engine/risk-metrics`
- `GET /risk-engine/risk-metrics/{risk_metric_id}`
- `PUT /risk-engine/risk-metrics/{risk_metric_id}`
- `DELETE /risk-engine/risk-metrics/{risk_metric_id}`

### Volatility Lab (`/volatility-lab`)

- File: `backend/app/modules/volatility_lab/routes.py`
- Registered in: `backend/app/api/router.py` with prefix `/volatility-lab`

CRUD (volatility forecasts):
- `POST /volatility-lab/volatility-forecasts`
- `GET /volatility-lab/volatility-forecasts`
- `GET /volatility-lab/volatility-forecasts/{forecast_id}`
- `PUT /volatility-lab/volatility-forecasts/{forecast_id}`
- `DELETE /volatility-lab/volatility-forecasts/{forecast_id}`

### Stat Arb Engine (`/stat-arb-engine`)

- File: `backend/app/modules/stat_arb_engine/routes.py`
- Registered in: `backend/app/api/router.py` with prefix `/stat-arb-engine`

CRUD (stat arb pairs):
- `POST /stat-arb-engine/stat-arb-pairs`
- `GET /stat-arb-engine/stat-arb-pairs`
- `GET /stat-arb-engine/stat-arb-pairs/{pair_id}`
- `PUT /stat-arb-engine/stat-arb-pairs/{pair_id}`
- `DELETE /stat-arb-engine/stat-arb-pairs/{pair_id}`

### Reporting (`/reporting`)

- File: `backend/app/modules/reporting/routes.py`
- Registered in: `backend/app/api/router.py` with prefix `/reporting`

CRUD (research reports):
- `POST /reporting/research-reports`
- `GET /reporting/research-reports`
- `GET /reporting/research-reports/{report_id}`
- `PUT /reporting/research-reports/{report_id}`
- `DELETE /reporting/research-reports/{report_id}`

### AI Assistant (`/ai-assistant`)

- File: `backend/app/modules/ai_assistant/routes.py`
- Registered in: `backend/app/api/router.py` with prefix `/ai-assistant`

CRUD (AI conversations):
- `POST /ai-assistant/ai-conversations`
- `GET /ai-assistant/ai-conversations`
- `GET /ai-assistant/ai-conversations/{conversation_id}`
- `PUT /ai-assistant/ai-conversations/{conversation_id}`
- `DELETE /ai-assistant/ai-conversations/{conversation_id}`

### Market Data (`/market-data`)

- File: `backend/app/modules/market_data/routes.py`
- Registered in: `backend/app/api/router.py` with prefix `/market-data`

CRUD (assets):
- `POST /market-data/assets`
- `GET /market-data/assets`
- `GET /market-data/assets/{asset_id}`
- `PUT /market-data/assets/{asset_id}`
- `DELETE /market-data/assets/{asset_id}`

CRUD (price bars):
- `POST /market-data/price-bars`
- `GET /market-data/price-bars`
- `GET /market-data/price-bars/{price_bar_id}`
- `PUT /market-data/price-bars/{price_bar_id}`
- `DELETE /market-data/price-bars/{price_bar_id}`

## Tech Stack

- **FastAPI** (HTTP API + OpenAPI/Swagger)
- **Pydantic** (schemas)
- **SQLAlchemy** (ORM)
- **Python-JOSE** (JWT)
- **Uvicorn** (ASGI server)
- **Redis** (declared in requirements; used by future caching/queueing)
- **Celery** (declared in requirements; used by future async jobs)

## Database Design

The project is wired for SQLAlchemy-based persistence:
- `backend/app/core/database.py` provides `database.init_db()` and a `get_db` dependency used by routes.

> Note: Module-specific SQLAlchemy models are expected in each module’s `models.py` (e.g., `backend/app/modules/<module>/models.py`). Current route handlers call module `services.py` functions, which in turn are expected to interact with the database models.

### Mermaid: Data Flow in a Typical Endpoint

```mermaid
flowchart LR
  A[API Route (routes.py)] --> B[Service (services.py)]
  B --> C[SQLAlchemy Models]
  C --> D[(DB)]
  B -->|response| A
```

## API Design

### Health
- `GET /health`

Defined in: `backend/app/main.py`.

### Swagger
- `GET /api/docs`

Configured in: `backend/app/main.py`.

## Installation

1. (Recommended) Create a virtual environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment (database, redis) as required by `backend/app/core/config.py` and `backend/app/core/database.py`.

## Local Development

Run the API server:

```bash
uvicorn app.main:app --reload
```

Swagger UI:
- http://127.0.0.1:8000/api/docs

## Docker Setup

This repository includes Docker artifacts (`backend/Dockerfile` and `backend/docker-compose.yml`).

Start services:

```bash
docker-compose up --build
```

## Database (PostgreSQL)

QuantOS uses the `DATABASE_URL` environment variable (see `backend/app/core/config.py`).

### Example `DATABASE_URL`

- `postgresql+psycopg2://user:pass@db:5432/quantos`

### Using Docker Compose

`backend/docker-compose.yml` already configures PostgreSQL and Redis and sets `DATABASE_URL` to the PostgreSQL connection string.

### `.env.example`

A PostgreSQL-focused environment example is available at `backend/.env.example`.


## Swagger Documentation

The API is documented via FastAPI automatically:
- OpenAPI JSON: `/api/openapi.json`
- Swagger UI: `/api/docs`

## Roadmap

- Alpha expression evaluation pipeline (parser/evaluator)
- Backtest execution orchestration
- Persisting results and reporting workflows
- Authentication hardening (JWT issuance + guards)
- Background jobs (Celery) for long-running computations

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Follow the existing module structure:
   - `routes.py` for endpoints
   - `schemas.py` for request/response models
   - `services.py` for business logic
   - `models.py` for persistence
4. Add tests for new functionality

---

Built for research-to-production iteration—QuantOS aims to keep experimentation fast while maintaining a production-ready interface.

