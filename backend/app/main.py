from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import config, database
from app.api.router import router
from app.core.logging import setup_logging

app = FastAPI(
    title="QuantOS",
    description="Quantitative Trading Platform",
    version=config.settings.APP_VERSION,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
setup_logging()

# Initialize database
database.init_db()

# Register all API routes
app.include_router(router)


@app.get(
    "/health",
    tags=["System"],
    summary="Health Check",
)
def health_check():
    return {
        "status": "ok",
        "app": config.settings.APP_NAME,
        "version": config.settings.APP_VERSION,
    }


@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
