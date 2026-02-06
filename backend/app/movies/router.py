# app/movies/router.py
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, status, Depends, BackgroundTasks
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.movie import Movie
from app.movies.service import movie_service
from app.movies.archiveOrg_service import ArchiveOrgService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/movies", tags=["movies"])

# Initialize service
# archive_service = ArchiveOrgService()


@router.get("/search")
async def search_movies(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=50, description="Results per page"),
    use_cache: bool = Query(True, description="Use cached results if available"),
    db: AsyncSession = Depends(get_db)
):
    """
    Search for movies with caching strategy.
    
    Example: GET /api/movies/search?q=night+living+dead&page=1&limit=20
    """
    if not q or len(q.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Query parameter 'q' must be at least 2 characters"
        )
    
    try:
        result = await movie_service.search_movies(
            db=db,
            query=q.strip(),
            page=page,
            limit=limit,
            use_cache=use_cache
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/popular")
async def get_popular_movies(
    limit: int = Query(20, ge=1, le=100, description="Number of movies"),
    page: int = Query(1, ge=1, description="Page number"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get popular movies from cache.
    These are updated weekly by a cron job.
    """
    try:
        offset = (page - 1) * limit
        movies = await movie_service.get_popular_movies(db, limit, offset)
        
        return {
            "page": page,
            "limit": limit,
            "total": len(movies),
            "movies": [movie.get_basic_info() for movie in movies]
        }
        
    except Exception as e:
        logger.error(f"Error fetching popular movies: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch popular movies"
        )


@router.post("/popular/refresh")
async def refresh_popular_movies(
    background_tasks: BackgroundTasks,
    limit: int = Query(50, ge=10, le=200, description="Number of movies to fetch"),
    db: AsyncSession = Depends(get_db)
):
    """
    Manually trigger refresh of popular movies.
    Usually called by cron job weekly.
    """
    # Run in background to avoid timeout
    background_tasks.add_task(
        movie_service.fetch_and_store_popular_movies,
        db=db,
        limit=limit
    )
    
    return {
        "message": "Popular movies refresh started in background",
        "limit": limit,
        "status": "processing"
    }


@router.get("/{identifier}")
async def get_movie_details(
    identifier: str,
    refresh: bool = Query(False, description="Force refresh from external source"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get full movie details with caching.
    
    Example: GET /api/movies/night_of_the_living_dead?refresh=true
    """
    try:
        movie = await movie_service.get_movie_details(
            db=db,
            identifier=identifier,
            force_refresh=refresh
        )
        
        if not movie:
            raise HTTPException(
                status_code=404,
                detail=f"Movie '{identifier}' not found"
            )
        
        return {
            "movie": movie.get_full_info(),
            "source": "cache" if not refresh else "external",
            "metadata_age_days": (
                (datetime.utcnow() - movie.metadata_fetched_at).days
                if movie.metadata_fetched_at
                else None
            ),
            "is_available": movie.is_available(),
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching movie details: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch movie details: {str(e)}"
        )


@router.get("/{identifier}/torrent")
async def get_torrent_file(identifier: str):
    """
    Download the .torrent file for a movie.
    
    Example: GET /api/movies/night_of_the_living_dead/torrent
    """
    from fastapi.responses import Response
    
    try:
        archive_service = ArchiveOrgService()
        torrent_data = await archive_service.get_torrent_file(identifier)
        
        if not torrent_data:
            raise HTTPException(
                status_code=404,
                detail="Torrent file not found"
            )
        
        return Response(
            content=torrent_data,
            media_type="application/x-bittorrent",
            headers={
                "Content-Disposition": f"attachment; filename={identifier}.torrent"
            }
        )
        
    except Exception as e:
        logger.error(f"Error downloading torrent: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to download torrent: {str(e)}"
        )


@router.post("/cache/cleanup")
async def cleanup_cache(
    days_threshold: int = Query(90, ge=30, le=365, description="Days of inactivity"),
    db: AsyncSession = Depends(get_db)
):
    """
    Clean up stale cached movies.
    Should be called periodically by cron job.
    """
    try:
        result = await movie_service.cleanup_stale_cache(
            db=db,
            days_threshold=days_threshold
        )
        
        return {
            "message": "Cache cleanup completed",
            **result
        }
        
    except Exception as e:
        logger.error(f"Cache cleanup error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Cache cleanup failed: {str(e)}"
        )


@router.get("/stats/cache")
async def get_cache_stats(db: AsyncSession = Depends(get_db)):
    """
    Get caching statistics.
    """
    from sqlalchemy import func, select
    
    try:
        # Total movies in cache
        total_stmt = select(func.count()).select_from(Movie)
        total_result = await db.execute(total_stmt)
        total = total_result.scalar()
        
        # Popular movies count
        popular_stmt = select(func.count()).where(Movie.is_popular == True)
        popular_result = await db.execute(popular_stmt)
        popular = popular_result.scalar()
        
        # Downloaded movies count
        downloaded_stmt = select(func.count()).where(Movie.downloaded == True)
        downloaded_result = await db.execute(downloaded_stmt)
        downloaded = downloaded_result.scalar()
        
        # Average search hits
        avg_hits_stmt = select(func.avg(Movie.search_cache_hits))
        avg_hits_result = await db.execute(avg_hits_stmt)
        avg_hits = avg_hits_result.scalar() or 0
        
        return {
            "total_movies": total,
            "popular_movies": popular,
            "downloaded_movies": downloaded,
            "avg_search_hits": round(avg_hits, 2),
            "cache_efficiency": f"{popular}/{total} popular movies cached",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get cache stats"
        )