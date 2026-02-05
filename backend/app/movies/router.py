from fastapi import APIRouter, HTTPException, Query
from app.movies.archiveOrg_service import ArchiveOrgService
import httpx


router = APIRouter(prefix="/movies", tags=["movies"])


router = APIRouter(prefix="/api/movies", tags=["movies"])

# Initialize service
archive_service = ArchiveOrgService()





@router.get("/search")
async def search_movies(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=50, description="Results per page"),
):
    """
    Search for movies from Archive.org
    
    Example: GET /api/movies/search?q=night+living+dead&page=1&limit=20
    """
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
    
    results = await archive_service.search_movies(q, page, limit)
    
    return {
        "query": q,
        "page": page,
        "limit": limit,
        "results": results,
        "total": len(results),
    }


@router.get("/{identifier}")
async def get_movie_details(identifier: str):
    """
    Get detailed information about a specific movie
    
    Example: GET /api/movies/night_of_the_living_dead
    """
    movie = await archive_service.get_movie_details(identifier)
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie


@router.get("/{identifier}/torrent")
async def get_torrent_file(identifier: str):
    """
    Download the .torrent file for a movie
    
    Example: GET /api/movies/night_of_the_living_dead/torrent
    """
    from fastapi.responses import Response
    
    torrent_data = await archive_service.get_torrent_file(identifier)
    
    if not torrent_data:
        raise HTTPException(status_code=404, detail="Torrent file not found")
    
    return Response(
        content=torrent_data,
        media_type="application/x-bittorrent",
        headers={
            "Content-Disposition": f"attachment; filename={identifier}.torrent"
        }
    )
    

