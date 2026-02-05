import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.video import Video, StatusType
from app.models.movie import Movie
from app.movies.services.torrent_manager import torrent_manager
from datetime import datetime


class DownloadService:
    """
    Service to manage torrent downloads in the background.
    Coordinates between TorrentManager and Database.
    """

    @staticmethod
    async def start_download(
        movie_id: str, magnet_link: str, db: AsyncSession
    ) -> Video:
        """
        Start downloading a movie torrent.

        Steps:
        1. Check if movie exists
        2. Create or update Video record
        3. Start torrent download
        4. Return Video record
        """

        # 1. Verify movie exists
        stmt = select(Movie).where(Movie.id == movie_id)
        result = await db.execute(stmt)
        movie = result.scalar_one_or_none()

        if not movie:
            raise ValueError(f"Movie {movie_id} not found")

        # 2. Check if Video record exists
        stmt = select(Video).where(Video.movie_id == movie_id)
        result = await db.execute(stmt)
        video = result.scalar_one_or_none()

        if video:
            # Video already exists - check status
            if video.status == StatusType.READY:
                # Already downloaded
                return video
            elif video.status == StatusType.DOWNLOADING:
                # Already downloading
                return video
            else:
                # Failed or other status - restart
                video.status = StatusType.DOWNLOADING
                video.progress = 0
        else:
            # Create new Video record
            video = Video(
                movie_id=movie_id,
                file_path=f"/app/videos/{movie_id}/",
                status=StatusType.DOWNLOADING,
                progress=0,
            )
            db.add(video)

        await db.commit()
        await db.refresh(video)

        # 3. Start torrent download in TorrentManager
        success = torrent_manager.start_download(
            movie_id=movie_id, magnet_link=magnet_link
        )

        if not success:
            video.status = StatusType.ERROR
            await db.commit()
            raise RuntimeError(f"Failed to start download for {movie_id}")

        return video

    @staticmethod
    async def update_download_progress(movie_id: str, db: AsyncSession):
        """
        Update download progress in database.
        Called periodically by background task.
        """

        # Get status from TorrentManager
        status = torrent_manager.get_status(movie_id)

        if not status:
            return

        # Get Video record
        stmt = select(Video).where(Video.movie_id == movie_id)
        result = await db.execute(stmt)
        video = result.scalar_one_or_none()

        if not video:
            return

        # Update progress
        video.progress = status["progress"]

        # Update status based on progress
        if status["progress"] >= 100:
            video.status = StatusType.READY
            video.downloaded_at = datetime.utcnow()

            # Get actual file path
            file_path = torrent_manager.get_file_path(movie_id)
            if file_path:
                video.file_path = str(file_path)
                video.file_size = file_path.stat().st_size

                # Get video duration using ffprobe (will implement later)
                # video.duration = await get_video_duration(file_path)

        await db.commit()

    @staticmethod
    async def monitor_downloads(db: AsyncSession):
        """
        Background task that monitors all active downloads.
        Updates database with current progress.
        """

        while True:
            try:
                # Get all videos with status "downloading"
                stmt = select(Video).where(Video.status == StatusType.DOWNLOADING)
                result = await db.execute(stmt)
                videos = result.scalars().all()

                # Update each one
                for video in videos:
                    await DownloadService.update_download_progress(video.movie_id, db)

                # Wait 5 seconds before next check
                await asyncio.sleep(5)

            except Exception as e:
                print(f"Error in monitor_downloads: {e}")
                await asyncio.sleep(5)


download_service = DownloadService()
