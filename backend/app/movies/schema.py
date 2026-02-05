from pydantic import BaseModel


class StartDownloadRequest(BaseModel):
    """Request body for starting a download"""

    magnet_link: str


class DownloadStatusResponse(BaseModel):
    """Download status response"""

    movie_id: str
    status: str
    progress: int
    download_rate: int  # bytes/s
    upload_rate: int  # bytes/s
    total_download: int
    total_size: int
    eta_seconds: int
    num_peers: int
    num_seeds: int
    is_streamable: bool
