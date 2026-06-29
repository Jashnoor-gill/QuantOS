# QuantOS Architecture

## Overview
QuantOS is a quantitative trading platform consisting of a FastAPI backend and a React + TypeScript frontend.

## High-level components
- **Frontend (React/Vite/TS)**: SPA with route-based pages (Dashboard, Market Data, Alpha Lab, etc.).
- **Backend (FastAPI/Python)**: REST APIs grouped by module (auth, engines, reporting, etc.).
- **Persistence (SQLAlchemy + SQLite/SQL)**: User and domain models stored in a relational database.
- **Security (JWT)**: Access tokens are used to protect API endpoints.

## Runtime flow
1. User authenticates via `POST /auth/login`.
2. Frontend stores the JWT and attaches it to subsequent API calls.
3. Protected endpoints validate the token server-side.

## Folder mapping
- `backend/app/core/*` — app setup, config, database, security helpers.
- `backend/app/modules/*` — feature modules exposing route handlers.
- `frontend/src/pages/*` — React pages.
- `frontend/src/context/*` — React context providers (auth).
- `frontend/src/routes/*` — top-level route configuration.

## Notes
This document is a project-level architecture description intended for deployment and onboarding.
