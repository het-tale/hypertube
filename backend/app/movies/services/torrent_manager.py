import libtorrent as lt
import os
from typing import Dict, Optional
from pathlib import Path


class TorrentManager:
    """
    Manages torrent downloads to local filesystem.

    This class ONLY downloads to disk.
    It does NOT stream video to browser.
    """

    def __init__(self):
        self.session = lt.session()
        settings = {
            "download_rate_limit": int(os.getenv("MAX_DOWNLOAD_SPEED", 0)),
            "upload_rate_limit": int(os.getenv("MAX_UPLOAD_SPEED", 0)),
            "connections_limit": 200,
            "active_downloads": 5,
            "active_seeds": 5,
            "enable_dht": True,
            "enable_lsd": True,
            "enable_upnp": True,
            "enable_natpmp": True,
        }
        self.session.apply_settings(settings)

        self.session.add_dht_router("router.bittorrent.com", 6881)
        self.session.add_dht_router("dht.transmissionbt.com", 6881)

        self.active_downloads: Dict[str, lt.torrent_handle] = {}

        self.download_dir = Path(os.getenv("DOWNLOAD_DIR", "/app/videos"))
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def start_download(
        self, movie_id: str, magnet_link: str, torrent_file: Optional[bytes] = None
    ) -> bool:
        """
        Start downloading a torrent to local filesystem.

        Args:
            movie_id: Unique movie identifier
            magnet_link: Magnet URI
            torrent_file: Optional .torrent file content

        Returns:
            True if download started successfully
        """

        movie_dir = self.download_dir / movie_id
        movie_dir.mkdir(parents=True, exist_ok=True)

        params = {
            "save_path": str(movie_dir),
            "storage_mode": lt.storage_mode_t.storage_mode_allocate,
        }

        try:
            if torrent_file:
                torrent_info = lt.torrent_info(torrent_file)
                params["ti"] = torrent_info
                handle = self.session.add_torrent(params)
            else:
                handle = lt.add_magnet_uri(self.session, magnet_link, params)

            handle.set_sequential_download(True)

            if handle.has_metadata():
                self._set_piece_priorities(handle)

            self.active_downloads[movie_id] = handle

            return True

        except Exception as e:
            print(f"Error starting download for {movie_id}: {e}")
            return False

    def _set_piece_priorities(self, handle: lt.torrent_handle):
        """
        Set piece download priorities.

        Priority 0 = don't download
        Priority 1-7 = increasing priority

        Strategy:
        - First 5% of pieces: Priority 7 (highest) - for streaming start
        - Last 5% of pieces: Priority 6 - for metadata
        - Middle pieces: Priority 4 (normal)
        """
        if not handle.has_metadata():
            return

        torrent_info = handle.torrent_file()
        num_pieces = torrent_info.num_pieces()

        first_pieces = int(num_pieces * 0.05)
        last_pieces = int(num_pieces * 0.05)

        for i in range(num_pieces):
            if i < first_pieces:
                handle.piece_priority(i, 7)
            elif i >= num_pieces - last_pieces:
                handle.piece_priority(i, 6)
            else:
                handle.piece_priority(i, 4)

    def get_status(self, movie_id: str) -> Optional[Dict]:
        """
        Get current download status for a movie.

        Returns:
            Dictionary with download statistics or None if not found
        """
        handle = self.active_downloads.get(movie_id)

        if not handle:
            return None

        status = handle.status()

        progress = int(status.progress * 100)

        download_rate = status.download_rate

        upload_rate = status.upload_rate

        total_download = status.total_done

        total_size = status.total_wanted

        if download_rate > 0:
            remaining_bytes = total_size - total_download
            eta_seconds = int(remaining_bytes / download_rate)
        else:
            eta_seconds = 0

        pieces = status.pieces
        num_pieces = len(pieces)
        downloaded_pieces = sum(pieces)

        return {
            "progress": progress,
            "download_rate": download_rate,
            "upload_rate": upload_rate,
            "total_download": total_download,
            "total_size": total_size,
            "eta_seconds": eta_seconds,
            "num_peers": status.num_peers,
            "num_seeds": status.num_seeds,
            "state": str(status.state),
            "paused": status.paused,
            "pieces_downloaded": downloaded_pieces,
            "pieces_total": num_pieces,
        }

    def is_streamable(self, movie_id: str, threshold: float = 0.05) -> bool:
        """
        Check if enough data has been downloaded to start streaming.

        Args:
            movie_id: Movie identifier
            threshold: Minimum progress required (0.05 = 5%)

        Returns:
            True if video can be streamed from partial file
        """
        handle = self.active_downloads.get(movie_id)

        if not handle:
            return False

        status = handle.status()

        if status.progress < threshold:
            return False

        if not handle.has_metadata():
            return False

        pieces = status.pieces
        required_pieces = int(len(pieces) * threshold)

        for i in range(min(required_pieces, len(pieces))):
            if not pieces[i]:
                return False

        return True

    def pause_download(self, movie_id: str) -> bool:
        """Pause a download."""
        handle = self.active_downloads.get(movie_id)
        if handle:
            handle.pause()
            return True
        return False

    def resume_download(self, movie_id: str) -> bool:
        """Resume a paused download."""
        handle = self.active_downloads.get(movie_id)
        if handle:
            handle.resume()
            return True
        return False

    def cancel_download(self, movie_id: str) -> bool:
        """
        Cancel and remove a download.
        Does NOT delete files - use separately.
        """
        handle = self.active_downloads.get(movie_id)
        if handle:
            self.session.remove_torrent(handle)
            del self.active_downloads[movie_id]
            return True
        return False

    def get_file_path(self, movie_id: str) -> Optional[Path]:
        """
        Get the path to the downloaded video file.

        Returns the largest file in the movie directory
        (assumes it's the video file).
        """
        movie_dir = self.download_dir / movie_id

        if not movie_dir.exists():
            return None

        files = list(movie_dir.glob("*"))
        if not files:
            return None

        largest_file = max(files, key=lambda f: f.stat().st_size if f.is_file() else 0)

        return largest_file if largest_file.is_file() else None


torrent_manager = TorrentManager()
