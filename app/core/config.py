"""Core configuration settings using Pydantic v2."""
from typing import List, Literal

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    DATABASE_URL: PostgresDsn

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application
    APP_NAME: str = "FastAPI Auth Template"
    DEBUG: bool = False
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    # Cookie Settings
    COOKIE_SECURE: bool = True
    COOKIE_SAMESITE: Literal['lax', 'strict', 'none'] = "lax"
    COOKIE_DOMAIN: str | None = None
    COOKIE_HTTPONLY: bool = True

    @property
    def allowed_origins_list(self) -> List[str]:
        """Get ALLOWED_ORIGINS as a list."""
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
        # Fallback for unexpected types
        return []

    @property
    def database_url_asyncpg(self) -> str:
        """Get database URL as string for asyncpg."""
        return str(self.DATABASE_URL)


# Global settings instance
settings = Settings() # type: ignore