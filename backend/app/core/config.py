from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "QuantOS"
    APP_VERSION: str = "1.0.0"

    # Database
    # Default kept as SQLite for local/offline dev, but deployment should override via env var.
    DATABASE_URL: str = "sqlite:///./quantos.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security (JWT)
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"



settings = Settings()




