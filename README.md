# QuantOS

QuantOS is a quantitative research workspace for market data, factor analysis, alpha research, strategy development, backtesting, portfolio construction, risk, and reporting.

## Stack

- React, TypeScript, Vite, Tailwind CSS, Recharts
- FastAPI, SQLAlchemy, PostgreSQL, Redis
- Docker Compose with Nginx serving the frontend

## Features

- Dashboard with quantitative KPIs and charts
- Market data, factors, alphas, strategies, backtests, portfolios, risk, analytics, reports, and Alpha Lab views
- Browser-persistent Demo mode with sample data across the application
- FastAPI documentation at `/api/docs`
- Health check at `/api/health`

## Demo mode

Demo mode is enabled by default for first-time visitors. Use the **Demo mode** toggle in the top-right navigation to switch between local sample data and live API data. Demo data is frontend-only and does not write to the database.

## Run locally with Docker

```bash
cp .env.example .env
docker compose up -d --build
```

Open `http://localhost` after the containers start.

Check services and logs:

```bash
docker compose ps
docker compose logs -f --tail=100
```

## Run locally without Docker

Start the backend:

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

In a second terminal, start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` requests to the backend.

## AWS deployment

The recommended low-cost deployment runs the complete Docker Compose stack on one free-tier-eligible EC2 instance. Follow [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md) for EC2 setup, security-group rules, environment variables, startup, updates, and logs.

The public deployment should expose HTTP port 80 only. Keep PostgreSQL and Redis private to the Docker network. Add HTTPS before using real credentials or trading workflows.

## Project layout

```text
backend/    FastAPI application and domain modules
frontend/   React application and production Nginx image
docs/       Architecture and project documentation
```

## Production note

QuantOS is a research and paper-trading platform. Validate data quality, authentication, authorization, execution, monitoring, and risk controls before using it with real capital.