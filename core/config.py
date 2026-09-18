
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Shipment Management API"
    ENVIRONMENT: str = "development"

    # Database Settings (Loaded directly from .env)
    DATABASE_URL: Optional[str] = None

    # Postgres Individual Variables (loaded from .env)
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PORT: Optional[int] = 5432
    POSTGRES_HOST: Optional[str] = "localhost"  # Matches POSTGRES_HOST in .env
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    # Optional pre-formatted Postgres URL
    POSTGRES_URL: Optional[str] = None

    @property
    def database_url(self) -> str:
        """Dynamically construct Postgres async URL based on available settings."""
        # 1. Use DATABASE_URL if directly provided in .env
        if self.DATABASE_URL:
            return self.DATABASE_URL

        # 2. Use pre-formatted POSTGRES_URL if provided
        if self.POSTGRES_URL:
            if self.POSTGRES_URL.startswith("postgresql://"):
                return self.POSTGRES_URL.replace(
                    "postgresql://", "postgresql+asyncpg://", 1
                )
            return self.POSTGRES_URL

        # 3. Build URL from individual environment variables if present
        if self.POSTGRES_USER and self.POSTGRES_PASSWORD and self.POSTGRES_DB:
            return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

        raise ValueError(
            "No database configuration found! Ensure DATABASE_URL or individual POSTGRES_* variables are set in .env."
        )

    DEVELOPMENT_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8501",
        "http://127.0.0.1:5500",
    ]

    PRODUCTION_ORIGINS: list[str] = [
        "https://mydomain.com",
        "https://admin.mydomain.com",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        if self.ENVIRONMENT.lower() == "development":
            return self.DEVELOPMENT_ORIGINS
        return self.PRODUCTION_ORIGINS


settings = Settings()