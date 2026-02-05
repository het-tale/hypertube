from fastapi import APIRouter, HTTPException, Query, status, Depends
from app.movies.archiveOrg_service import ArchiveOrgService
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.session import get_db
from app.movies.service import movie_service
import httpx


router = APIRouter(prefix="/movies", tags=["movies"])




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
    


# @router.get("/{movie_id}")
# async def get_movie_detail(movie_id: str, db: AsyncSession = Depends(get_db)):
#     """
#     Get detailed information about a Movie

#     Args:
#         movie_id (str): The id of the movie we looking for
#         db (AsyncSession): Database dependency
#     """
#     movie = movie_service.get_movie(movie_id, db)
#     if not movie:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Movie with id '{movie_id}' not found",
#         )
#     response = {
#         "id": movie.id,
#         "year": movie.year,
#         "rating": movie.rating,
#         "genres": movie.genres,
#         "summary": movie.summary,
#         "poster_url": movie.poster_url,
#         "duration": movie.duration,
#         "source": movie.source,
#         "torrent_url": movie.torrent_hash,
#         "magnet_link": movie.magnet_link,
#         "cast": [
#             {
#                 "id": c.id,
#                 "name": c.name,
#                 "role": c.role,
#                 "character": c.character,
#                 "order": c.display_order,
#             }
#             for c in sorted(
#                 movie.cast, key=lambda x: x.display_order if x.display_order else 999
#             )
#         ],
#         "video": (
#             {
#                 "status": movie.video.status,
#                 "file_path": movie.video.file_path,
#                 "progress": movie.video.progress,
#                 "downloaded_at": (
#                     movie.video.downloaded_at.isoformat()
#                     if movie.video.downloaded_at
#                     else None
#                 ),
#                 "file_size": movie.video.file_size,
#                 "duration": movie.video.duration,
#                 "is_streamable": movie.video.is_streamable,
#             }
#             if movie.video
#             else None
#         ),
#         "comments": [
#             {
#                 "id": c.id,
#                 "user": {
#                     "id": c.user.id,
#                     "username": c.user.username,
#                     "profile_picture": c.user.profile_picture,
#                 },
#                 "content": c.content,
#                 "created_at": c.created_at.isoformat(),
#                 "updated_at": c.updated_at.isoformat() if c.updated_at else None,
#             }
#             for c in sorted(movie.comment, key=lambda x: x.created_at, reverse=True)
#         ],
#         "comments_count": len(movie.comment),
#         "created_at": movie.created_at.isoformat(),
#         "updated_at": movie.updated_at.isoformat() if movie.updated_at else None,
#     }
#     return response
