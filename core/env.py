from functools import lru_cache
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core
    DEBUG: bool = False
    SECRET_KEY: str = Field(..., min_length=20)
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    CSRF_TRUSTED_ORIGINS: List[str] = []

    # DB
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ...
    POSTGRES_DB: str = "postgres_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
