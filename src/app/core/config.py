"""Application configuration using pydantic-settings."""

from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "FastAPI Template"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"

    # Database
    database_url: str
    database_echo: bool = False

    # Redis
    redis_url: str

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str] | Any:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            # Handle JSON string format
            import json

            try:
                parsed: list[str] = json.loads(v)
                return parsed
            except json.JSONDecodeError:
                # Handle comma-separated string
                result: list[str] = [origin.strip() for origin in v.split(",")]
                return result
        return v

    # Logging
    log_level: str = "INFO"


# Global settings instance
settings = Settings()
