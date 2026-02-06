# app/core/scheduler.py
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.db.session import async_session_maker
from app.movies.service import movie_service
import logging

logger = logging.getLogger(__name__)


class MovieCacheScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
    
    async def refresh_popular_movies(self):
        """Weekly job to refresh popular movies."""
        logger.info("Starting weekly popular movies refresh...")
        
        try:
            async with async_session_maker() as db:
                result = await movie_service.fetch_and_store_popular_movies(
                    db=db,
                    limit=100
                )
                logger.info(f"Popular movies refresh completed: {result}")
        except Exception as e:
            logger.error(f"Failed to refresh popular movies: {e}")
    
    async def cleanup_stale_cache(self):
        """Monthly job to clean up stale cache."""
        logger.info("Starting monthly cache cleanup...")
        
        try:
            async with async_session_maker() as db:
                result = await movie_service.cleanup_stale_cache(
                    db=db,
                    days_threshold=90
                )
                logger.info(f"Cache cleanup completed: {result}")
        except Exception as e:
            logger.error(f"Failed to cleanup cache: {e}")
    
    def start(self):
        """Start the scheduler with configured jobs."""
        # Refresh popular movies every Sunday at 3 AM
        self.scheduler.add_job(
            self.refresh_popular_movies,
            CronTrigger(day_of_week='sun', hour=3, minute=0),
            id='refresh_popular_movies',
            name='Refresh popular movies weekly',
            replace_existing=True
        )
        
        # Cleanup stale cache every 1st of month at 4 AM
        self.scheduler.add_job(
            self.cleanup_stale_cache,
            CronTrigger(day=1, hour=4, minute=0),
            id='cleanup_stale_cache',
            name='Cleanup stale cache monthly',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("Movie cache scheduler started")
    
    def shutdown(self):
        """Shutdown the scheduler."""
        self.scheduler.shutdown()
        logger.info("Movie cache scheduler stopped")


# Global scheduler instance
scheduler = MovieCacheScheduler()