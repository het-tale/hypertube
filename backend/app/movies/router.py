from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.db.session import get_db
from app.models.movie import Movie
from app.models.video import Video
from app.movies.schema import DownloadStatusResponse, StartDownloadRequest
from app.movies.service import movie_service
from app.movies.services.download_service import download_service
from app.movies.services.torrent_manager import torrent_manager

movie_router = APIRouter(prefix="/movies", tags=["Movies"])


@movie_router.get("/{movie_id}")
async def get_movie_detail(movie_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get detailed information about a Movie

    Args:
        movie_id (str): The id of the movie we looking for
        db (AsyncSession): Database dependency
    """
    movie = movie_service.get_movie(movie_id, db)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id '{movie_id}' not found",
        )
    response = {
        "id": movie.id,
        "year": movie.year,
        "rating": movie.rating,
        "genres": movie.genres,
        "summary": movie.summary,
        "poster_url": movie.poster_url,
        "duration": movie.duration,
        "source": movie.source,
        "torrent_url": movie.torrent_hash,
        "magnet_link": movie.magnet_link,
        "cast": [
            {
                "id": c.id,
                "name": c.name,
                "role": c.role,
                "character": c.character,
                "order": c.display_order,
            }
            for c in sorted(
                movie.cast, key=lambda x: x.display_order if x.display_order else 999
            )
        ],
        "video": (
            {
                "status": movie.video.status,
                "file_path": movie.video.file_path,
                "progress": movie.video.progress,
                "downloaded_at": (
                    movie.video.downloaded_at.isoformat()
                    if movie.video.downloaded_at
                    else None
                ),
                "file_size": movie.video.file_size,
                "duration": movie.video.duration,
                "is_streamable": movie.video.is_streamable,
            }
            if movie.video
            else None
        ),
        "comments": [
            {
                "id": c.id,
                "user": {
                    "id": c.user.id,
                    "username": c.user.username,
                    "profile_picture": c.user.profile_picture,
                },
                "content": c.content,
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat() if c.updated_at else None,
            }
            for c in sorted(movie.comment, key=lambda x: x.created_at, reverse=True)
        ],
        "comments_count": len(movie.comment),
        "created_at": movie.created_at.isoformat(),
        "updated_at": movie.updated_at.isoformat() if movie.updated_at else None,
    }
    return response


@movie_router.post("/{movie_id}/download", status_code=status.HTTP_202_ACCEPTED)
async def start_download(
    movie_id: str,
    request: StartDownloadRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Start downloading a movie torrent.

    Returns immediately while download happens in background.
    Use GET /{movie_id}/download-status to check progress.
    """

    # Verify movie exists
    stmt = select(Movie).where(Movie.id == movie_id)
    result = await db.execute(stmt)
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie {movie_id} not found"
        )

    # Check if already downloaded
    stmt = select(Video).where(Video.movie_id == movie_id)
    result = await db.execute(stmt)
    video = result.scalar_one_or_none()

    if video and video.status == "ready":
        return {
            "message": "Video already downloaded",
            "movie_id": movie_id,
            "status": "ready",
            "progress": 100,
        }

    # Start download
    try:
        video = await download_service.start_download(
            movie_id=movie_id, magnet_link=request.magnet_link, db=db
        )

        return {
            "message": "Download started",
            "movie_id": movie_id,
            "status": video.status,
            "progress": video.progress,
        }

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@movie_router.get("/{movie_id}/download-status", response_model=DownloadStatusResponse)
async def get_download_status(movie_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get current download status for a movie.

    Frontend should poll this endpoint every 2-5 seconds
    to update progress bar.
    """

    # Get Video record from database
    stmt = select(Video).where(Video.movie_id == movie_id)
    result = await db.execute(stmt)
    video = result.scalar_one_or_none()

    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No download found for movie {movie_id}",
        )

    # Get real-time status from TorrentManager
    torrent_status = torrent_manager.get_status(movie_id)

    if not torrent_status:
        # Download not active in TorrentManager
        # Return database status only
        return DownloadStatusResponse(
            movie_id=movie_id,
            status=video.status,
            progress=video.progress,
            download_rate=0,
            upload_rate=0,
            total_download=video.file_size or 0,
            total_size=video.file_size or 0,
            eta_seconds=0,
            num_peers=0,
            num_seeds=0,
            is_streamable=(video.status == "ready"),
        )

    # Return real-time torrent status
    return DownloadStatusResponse(
        movie_id=movie_id,
        status=video.status,
        progress=torrent_status["progress"],
        download_rate=torrent_status["download_rate"],
        upload_rate=torrent_status["upload_rate"],
        total_download=torrent_status["total_download"],
        total_size=torrent_status["total_size"],
        eta_seconds=torrent_status["eta_seconds"],
        num_peers=torrent_status["num_peers"],
        num_seeds=torrent_status["num_seeds"],
        is_streamable=torrent_manager.is_streamable(movie_id),
    )


@movie_router.post("/{movie_id}/download/pause")
async def pause_download(movie_id: str, db: AsyncSession = Depends(get_db)):
    """Pause an ongoing download."""

    success = torrent_manager.pause_download(movie_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No active download found for {movie_id}",
        )

    return {"message": "Download paused", "movie_id": movie_id}


@movie_router.post("/{movie_id}/download/resume")
async def resume_download(movie_id: str, db: AsyncSession = Depends(get_db)):
    """Resume a paused download."""

    success = torrent_manager.resume_download(movie_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No paused download found for {movie_id}",
        )

    return {"message": "Download resumed", "movie_id": movie_id}


@movie_router.delete("/{movie_id}/download")
async def cancel_download(movie_id: str, db: AsyncSession = Depends(get_db)):
    """
    Cancel and delete a download.
    Also removes Video record from database.
    """

    # Cancel in TorrentManager
    torrent_manager.cancel_download(movie_id)

    # Delete Video record
    stmt = select(Video).where(Video.movie_id == movie_id)
    result = await db.execute(stmt)
    video = result.scalar_one_or_none()

    if video:
        await db.delete(video)
        await db.commit()

    return {"message": "Download cancelled", "movie_id": movie_id}
