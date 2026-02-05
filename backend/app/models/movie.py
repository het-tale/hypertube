# app/models/movie.py

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    Boolean, DateTime, Float, Integer, String, Text, JSON, Index
)
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.db.session import Base
from app.models.genre import movie_genres

if TYPE_CHECKING:
    from app.models.genre import Genre
    from app.models.cast import Cast
    from app.models.comment import Comment
    from app.models.watch_history import WatchHistory
    from app.models.subtitle import Subtitle
    from app.models.video import Video


class Movie(Base):
    """
    Movie model for storing movie metadata from external sources.
    
    Supports multiple sources (Archive.org, YTS, etc.) with source-specific
    fields stored in JSON for flexibility.
    """
    __tablename__ = "movies"

    # ============================================================================
    # PRIMARY FIELDS
    # ============================================================================
    
    # Primary key - unique identifier from source
    # e.g., "charlie_chaplin_film_fest" for Archive.org
    # or "tt1375666" for IMDb/YTS
    id: Mapped[str] = mapped_column(
        String(255), 
        primary_key=True,
        comment="Unique identifier from source (Archive.org ID or IMDb ID)"
    )

    # ✅ ADDED: Source identifier for multi-source support
    source: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        index=True,
        comment="Data source: archive.org, yts, rarbg, etc."
    )

    # ============================================================================
    # BASIC MOVIE INFO (Common across all sources)
    # ============================================================================
    
    title: Mapped[str] = mapped_column(
        String(500),  # ⚠️ CHANGED: 255 → 500 (some titles are long)
        nullable=False,
        index=True  # ✅ ADDED: For search performance
    )
    

    description: Mapped[str | None] = mapped_column(
        Text, 
        nullable=True,
        comment="Movie plot/summary"
    )
    
    year: Mapped[int | None] = mapped_column(
        Integer, 
        nullable=True,
        index=True  # ✅ ADDED: For filtering by year
    )
    
    # Runtime in seconds (not minutes!)
    runtime: Mapped[int | None] = mapped_column(
        Integer, 
        nullable=True,
        comment="Duration in seconds"
    )
    
    director: Mapped[str | None] = mapped_column(
        String(255), 
        nullable=True
    )
    

    language: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
        index=True,
        comment="Language code (en, fr, es, etc.)"
    )
    
    poster_url: Mapped[str | None] = mapped_column(
        String(1000), 
        nullable=True
    )

    # ============================================================================
    # RATINGS (Multi-source support)
    # ============================================================================
    

    archive_rating: Mapped[float | None] = mapped_column(
        Float,  # ✅ FIXED: Was Integer
        nullable=True,
        comment="Rating from Archive.org (0-5 stars)"
    )
    
    # ✅ ADDED: IMDb rating (for YTS and other sources)
    imdb_rating: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        index=True,  # For filtering by rating
        comment="IMDb rating (0-10)"
    )
    
    # ✅ ADDED: IMDb ID for cross-referencing
    imdb_id: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        unique=True,
        index=True,
        comment="IMDb ID (e.g., tt1375666)"
    )

    # ============================================================================
    # SOURCE-SPECIFIC FIELDS (Archive.org)
    # ============================================================================
    
    archive_url: Mapped[str | None] = mapped_column(
        String(1000), 
        nullable=True,
        comment="Archive.org details page URL"
    )
    
    # Number of times downloaded from Archive.org
    downloads: Mapped[int] = mapped_column(
        Integer, 
        default=0, 
        nullable=False,
        comment="Download count from source"
    )
    
    num_reviews: Mapped[int] = mapped_column(
        Integer, 
        default=0, 
        nullable=False,
        comment="Number of reviews from source"
    )

    # ============================================================================
    # TORRENT INFO (Stored as JSON for flexibility)
    # ============================================================================
    
    # ✅ ADDED: Store all available torrents as JSON
    # Allows multiple qualities, formats, sources
    torrents: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
        comment="Available torrents with quality, magnet links, seeders, etc."
    )
    # Example structure:
    # {
    #     "720p": {
    #         "quality": "720p",
    #         "magnet": "magnet:?xt=...",
    #         "torrent_url": "https://...",
    #         "seeders": 150,
    #         "leechers": 20,
    #         "size_bytes": 900000000,
    #         "file_format": "mp4"
    #     },
    #     "1080p": { ... }
    # }

    # ============================================================================
    # DOWNLOAD STATUS (Critical for Hypertube functionality)
    # ============================================================================
    
    # ✅ ADDED: Is file downloaded and ready to stream?
    downloaded: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,  # For filtering available movies
        comment="Whether movie file is downloaded and available"
    )
    
    # ✅ ADDED: Download status tracking
    download_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Download status: null, queued, downloading, processing, complete, failed"
    )
    
    # ✅ ADDED: Download progress (0-100)
    download_progress: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Download progress percentage (0-100)"
    )
    
    # ✅ ADDED: Error message if download failed
    download_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Error message if download failed"
    )
    
    # ✅ ADDED: Path to downloaded file on server
    file_path: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
        comment="Path to downloaded video file on server"
    )
    
    # ✅ ADDED: File size in bytes
    file_size: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Downloaded file size in bytes"
    )
    
    # ✅ ADDED: Which quality was downloaded
    downloaded_quality: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Quality of downloaded file (720p, 1080p, etc.)"
    )

    # ============================================================================
    # WATCH TRACKING (For 30-day cleanup rule)
    # ============================================================================
    
    # ✅ ADDED: When was this movie last watched by ANY user
    last_watched_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True,  # For cleanup queries
        comment="Last time any user watched this movie"
    )
    
    # ✅ ADDED: Total view count across all users
    view_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Total number of times movie was watched"
    )

    # ============================================================================
    # METADATA TIMESTAMPS
    # ============================================================================
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="When movie was added to database"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Last metadata update"
    )

    # ============================================================================
    # RELATIONSHIPS
    # ============================================================================
    
    # Genres (many-to-many)
    genres: Mapped[list["Genre"]] = relationship(
        "Genre",
        secondary=movie_genres,
        back_populates="movies",
        lazy="selectin"  # ✅ ADDED: Eager load genres
    )
    
    # Cast members
    cast: Mapped[list["Cast"]] = relationship(
        "Cast",
        back_populates="movie",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # ⚠️ CHANGED: video → videos (one movie can have multiple video files)
    videos: Mapped[list["Video"]] = relationship(
        "Video",
        back_populates="movie",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # Comments
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="movie",
        cascade="all, delete-orphan",
        order_by="Comment.created_at.desc()"  # ✅ ADDED: Order by newest first
    )
    
    # Watch history (per user)
    watch_history: Mapped[list["WatchHistory"]] = relationship(
        "WatchHistory",
        back_populates="movie",
        cascade="all, delete-orphan"
    )
    
    # Subtitles
    subtitles: Mapped[list["Subtitle"]] = relationship(
        "Subtitle",
        back_populates="movie",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # ============================================================================
    # TABLE INDEXES (For performance)
    # ============================================================================
    
    __table_args__ = (
        # ✅ ADDED: Composite index for cleanup queries
        Index(
            'ix_movies_cleanup',
            'downloaded',
            'last_watched_at',
            postgresql_where="downloaded = true"
        ),
        # ✅ ADDED: Index for popular movies
        Index('ix_movies_popular', 'view_count', 'archive_rating'),
        # ✅ ADDED: Index for search by title and year
        Index('ix_movies_search', 'title', 'year'),
    )

    # ============================================================================
    # HELPER METHODS
    # ============================================================================
    
    def __repr__(self) -> str:
        return f"<Movie(id={self.id}, title={self.title}, source={self.source})>"
    
    def is_available(self) -> bool:
        """Check if movie is downloaded and ready to stream."""
        return self.downloaded and self.file_path is not None
    
    def needs_cleanup(self, days: int = 30) -> bool:
        """Check if movie should be deleted (not watched in X days)."""
        if not self.downloaded or not self.last_watched_at:
            return False
        
        days_since_watched = (datetime.utcnow() - self.last_watched_at).days
        return days_since_watched >= days
    
    def get_best_torrent(self, preferred_quality: str = "1080p") -> dict | None:
        """Get best available torrent, preferring given quality."""
        if not self.torrents:
            return None
        
        # Try preferred quality first
        if preferred_quality in self.torrents:
            return self.torrents[preferred_quality]
        
        # Fall back to any available quality
        available = list(self.torrents.keys())
        if available:
            return self.torrents[available[0]]
        
        return None