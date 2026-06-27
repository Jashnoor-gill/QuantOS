# QuantOS

A production-grade quantitative trading platform built with FastAPI, SQLAlchemy, and Redis.

## Features
- Modular monolith architecture
- JWT authentication
- PostgreSQL database
- Redis caching
- Health monitoring
- Docker support

## Installation
1. Create virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `uvicorn app.main:app --reload`

## Docker
```
docker-compose up --build
```

## API
- `/health` - Health check endpoint
- `/api/docs` - Swagger UI

> **Note**: This is a production-ready skeleton for QuantOS. All modules (auth, users, data_lab, etc.) will be implemented in subsequent steps.