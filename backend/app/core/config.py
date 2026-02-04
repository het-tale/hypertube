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
    APP_NAME: str = "Hypertube"
    DEBUG: bool = False
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    API_DOMAIN: str = "http://localhost:8000"

    # Cookie Settings
    COOKIE_SECURE: bool = True
    COOKIE_SAMESITE: Literal['lax', 'strict', 'none'] = "lax"
    COOKIE_DOMAIN: str | None = None
    COOKIE_HTTPONLY: bool = True




    # Oauth settings 42 
    OAUTH_42_CLIENT_ID: str
    OAUTH_42_CLIENT_SECRET: str
    OAUTH_42_REDIRECT_URI: str = "http://localhost:8000/auth/42/callback/"
    OAUTH_42_AUTHORIZE_URL: str = "https://api.intra.42.fr/oauth/authorize"
    OAUTH_42_TOKEN_URL: str = "https://api.intra.42.fr/oauth/token"
    OAUTH_42_USER_INFO_URL: str = "https://api.intra.42.fr/v2/me"
    
    # OAuth Settings - Google
    OAUTH_GOOGLE_CLIENT_ID: str
    OAUTH_GOOGLE_CLIENT_SECRET: str
    OAUTH_GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"
    OAUTH_GOOGLE_AUTHORIZE_URL: str = "https://accounts.google.com/o/oauth2/v2/auth"
    OAUTH_GOOGLE_TOKEN_URL: str = "https://oauth2.googleapis.com/token"
    OAUTH_GOOGLE_USER_INFO_URL: str = "https://www.googleapis.com/oauth2/v2/userinfo"


    #OAuth Settings - Discord

    OAUTH_DISCORD_CLIENT_ID: str
    OAUTH_DISCORD_CLIENT_SECRET: str
    OAUTH_DISCORD_REDIRECT_URI: str = "http://localhost:8000/auth/discord/callback"
    OAUTH_DISCORD_AUTHORIZE_URL: str = "https://discord.com/oauth2/authorize"
    OAUTH_DISCORD_TOKEN_URL: str = "https://discord.com/api/oauth2/token"
    OAUTH_DISCORD_USER_INFO_URL: str = "https://discord.com/api/oauth2/@me"


    #OAuth Settings - Github

    OAUTH_GITHUB_CLIENT_ID: str
    OAUTH_GITHUB_CLIENT_SECRET: str
    OAUTH_GITHUB_REDIRECT_URI: str = "http://localhost:8000/auth/github/callback"
    OAUTH_GITHUB_AUTHORIZE_URL: str = "https://github.com/login/oauth/authorize"
    OAUTH_GITHUB_TOKEN_URL: str = "https://github.com/login/oauth/access_token"
    OAUTH_GITHUB_USER_INFO_URL: str = "https://api.github.com/user"
    OAUTH_GITHUB_EMAIL_URL: str = "https://api.github.com/user/emails"


    #OAuth Settings - FACEBOOK

    # OAUTH_FACEBOOK_CLIENT_ID: str
    # OAUTH_FACEBOOK_CLIENT_SECRET: str
    # OAUTH_FACEBOOK_REDIRECT_URI: str = "http://localhost:8000/auth/FACEBOOK/callback"
    # OAUTH_FACEBOOK_AUTHORIZE_URL: str = "https://FACEBOOK.com/oauth2/authorize"
    # OAUTH_FACEBOOK_TOKEN_URL: str = "https://FACEBOOK.com/api/oauth2/token"
    # OAUTH_FACEBOOK_USER_INFO_URL: str = "https://discord.com/api/oauth2/users/@me"

    
    # Frontend URL (for redirects after OAuth)
    FRONTEND_URL: str = "http://localhost:3000"

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