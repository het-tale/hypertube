"""Main FastAPI application."""

from sched import scheduler
from fastapi import FastAPI, logger
from fastapi.middleware.cors import CORSMiddleware

import app
from app.auth.router import router as auth_router
from app.core.config import settings
from app.users.router import router as users_router
from app.Oauth.router import router as oauth_router
from app.movies.router import router as movies_router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.scheduler import scheduler




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

    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

    # Include routers
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(oauth_router)
    app.include_router(movies_router)


    @app.on_event("startup")
    async def startup_event():
        """Start background tasks on startup."""
        # Start the scheduler
        scheduler.start()
        # logger.info("Application started with scheduler")


    @app.on_event("shutdown")
    async def shutdown_event():
        """Clean shutdown."""
        scheduler.shutdown()
        # logger.info("Application shutdown complete")
    
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
