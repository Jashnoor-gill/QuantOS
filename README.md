# QuantOS

## Overview

QuantOS is a modular quantitative trading platform built with **FastAPI** and **SQLAlchemy**, designed to support research, strategy development, backtesting, risk analysis, and (eventually) live trading workflows.

## Architecture

### Backend (modular monolith)

The backend is organized as a modular monolith:
- Each domain feature lives in its own module under `backend/app/modules/<module_name>/`.
- Each module exposes an `APIRouter` in `routes.py`.
- `backend/app/api/router.py` aggregates module routers under stable URL prefixes.

Key entry points:
- `backend/app/main.py` — FastAPI app creation, CORS middleware, `database.init_db()`, and router inclusion.
- `backend/app/api/router.py` — router registration and URL prefixes.

### Frontend (React + TypeScript)

The frontend is a React + TypeScript SPA built with Vite. Pages live under `frontend/src/pages/` and routes under `frontend/src/routes/`.

## Backend Stack

- FastAPI
- SQLAlchemy
- Pydantic
- Python-JOSE (JWT)
- Uvicorn

## Frontend Stack

- React
- TypeScript
- Vite
- Tailwind (styling)
- Recharts (charts)

## Database

SQLAlchemy-based persistence. The app wires database initialization in:
- `backend/app/core/database.py` (via `database.init_db()` in `backend/app/main.py`).

## Authentication

Verified backend auth endpoints:
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

The frontend uses JWT storage in `localStorage` and protects application routes via `ProtectedRoute`.

## Analytics Engine

Module registered in `backend/app/api/router.py` under `/analytics`.

(See `backend/app/modules/analytics/` for module implementation.)

## Portfolio Optimization

Module registered in `backend/app/api/router.py` under `/portfolio-optimizer`.

(See `backend/app/modules/portfolio_optimizer/` for module implementation.)

## Market Data Engine

Module registered in `backend/app/api/router.py` under `/market-data`.

(See `backend/app/modules/market_data/` for module implementation.)

## Factor Engine

Module registered in `backend/app/api/router.py` under `/factor-engine`.

(See `backend/app/modules/factor_engine/` for module implementation.)

## Alpha Engine

Module registered in `backend/app/api/router.py` under `/alpha-engine`.

(See `backend/app/modules/alpha_engine/` for module implementation.)

## Strategy Engine

Module registered in `backend/app/api/router.py` under `/strategy-engine`.

(See `backend/app/modules/strategy_engine/` for module implementation.)

## Backtesting Engine

Module registered in `backend/app/api/router.py` under `/backtesting-engine`.

(See `backend/app/modules/backtesting_engine/` for module implementation.)

## Risk Engine

Module registered in `backend/app/api/router.py` under `/risk-engine`.

(See `backend/app/modules/risk_engine/` for module implementation.)

## Reporting

Module registered in `backend/app/api/router.py` under `/reporting`.

(See `backend/app/modules/reporting/` for module implementation.)

## AI Assistant

Module registered in `backend/app/api/router.py` under `/ai-assistant`.

(See `backend/app/modules/ai_assistant/` for module implementation.)

## Setup Instructions

### Backend

Run the API server:

- Swagger UI: `/api/docs`

```powershell
uvicorn app.main:app --reload
```

### Frontend

Build via:

```powershell
cd frontend
npm run build
```

## API Documentation

- Swagger: `GET /api/docs`
- OpenAPI JSON: `GET /api/openapi.json`

## Screenshots

This repository includes placeholder files under `docs/screenshots/`.

## Resume Description

See `docs/resume-description.md`.

## GitHub Description

(Repository description is derived from existing docs: `docs/architecture.md`, `docs/resume-description.md`, and `backend/README.md`.)

## Future Improvements

- Add expression/strategy evaluation pipelines (roadmap noted in repository docs).
- Add refresh-token flow.
- Expand authorization rules (RBAC).
- Replace any remaining mock data with real engine outputs.

