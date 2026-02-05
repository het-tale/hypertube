"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.core.config import settings
from app.users.router import router as users_router
from app.Oauth.router import router as oauth_router
from starlette.middleware.sessions import SessionMiddleware
from app.routers.main import main_router


def create_application() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        description="Video streaming app",
        version="1.0.0",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,  # Use your existing secret
        max_age=600,  # 10 minutes
    )

    # Include routers
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(oauth_router)
    app.include_router(main_router)

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "FastAPI Auth Template",
            "docs": "/docs",
            "version": "1.0.0",
        }

    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy"}

    return app


app = create_application()
