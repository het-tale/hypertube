"""Main FastAPI application."""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.core.config import settings
from app.users.router import router as users_router
from app.Oauth.router import router as oauth_router
from app.movies.router import movie_router
from starlette.middleware.sessions import SessionMiddleware

from app.movies.services.download_service import download_service
from app.db.session import get_db


def create_application() -> FastAPI:
    async def start_download_monitor():
        """Start the background task that monitors downloads."""
        while True:
            try:
                async for db in get_db():
                    await download_service.monitor_downloads(db)
                    break
            except Exception as e:
                print(f"Error in download monitor: {e}")
            await asyncio.sleep(5)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """
        Lifespan events - runs on startup and shutdown.
        Starts background tasks.
        """
        # Startup
        print("🚀 Starting Hypertube API...")

        # Start download monitoring task
        monitor_task = asyncio.create_task(start_download_monitor())

        yield

        # Shutdown
        print("🛑 Shutting down Hypertube API...")
        monitor_task.cancel()

    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        description="Video streaming app",
        version="1.0.0",
        lifespan=lifespan
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
    app.include_router(movie_router)

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
