# Postgres Database Settings and configuration using Pydantic BaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PORT: int
    POSTGRES_SERVER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file="./.env", 
        env_ignore_empty=True,
        extra="ignore",
        )

settings = DatabaseSettings()
print(settings.POSTGRES_USER)
print(settings.POSTGRES_PASSWORD)