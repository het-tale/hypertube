# app/models/movie.py
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import (
    Boolean, DateTime, Float, Integer, String, Text, JSON, Index, ARRAY
)
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
from app.db.session import Base
from app.models.cast import CastMember
from app.models.genre import movie_genres
from app.models.video import Video
from app.models.subtitle import Subtitle

if TYPE_CHECKING:
    from app.models.genre import Genre
    # from app.models.cast import CastMember
    from app.models.comment import Comment
    from app.models.watch_history import WatchHistory
    # from app.models.subtitle import Subtitle
    # from app.models.video import Video


class Movie(Base):
    __tablename__ = "movies"

    # ============================================================================
    # PRIMARY & SOURCE FIELDS
    # ============================================================================
    id: Mapped[str] = mapped_column(
        String(255), 
        primary_key=True,
        comment="Unique identifier from source (Archive.org ID or IMDb ID)"
    )
    
    source: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        index=True,
        comment="Data source: archive.org, yts, rarbg, etc."
    )

    # ============================================================================
    # CACHING & SEARCH FIELDS
    # ============================================================================
    
    search_cache_hits: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Number of times this movie was returned in search results"
    )
    
    last_searched_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="Last time this movie appeared in search results"
    )
    
    is_popular: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="Marked as popular movie (from weekly cron)"
    )
    
    popularity_rank: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Rank in popularity list (lower = more popular)"
    )
    
    popularity_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Computed popularity score (downloads * rating)"
    )
    
    # Cache metadata
    metadata_fetched_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="When full metadata was last fetched from external source"
    )
    
    metadata_freshness_days: Mapped[int] = mapped_column(
        Integer,
        default=30,
        nullable=False,
        comment="How many days before metadata should be refreshed"
    )

    # ============================================================================
    # BASIC MOVIE INFO
    # ============================================================================
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        index=True
    )
    
    description: Mapped[str | None] = mapped_column(
        Text, 
        nullable=True
    )
    
    year: Mapped[int | None] = mapped_column(
        Integer, 
        nullable=True,
        index=True
    )
    
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
        index=True
    )
    
    poster_url: Mapped[str | None] = mapped_column(
        String(1000), 
        nullable=True
    )

    # ============================================================================
    # RATINGS
    # ============================================================================
    archive_rating: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Rating from Archive.org (0-5 stars)"
    )
    
    imdb_rating: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        index=True
    )
    
    imdb_id: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        unique=True,
        index=True
    )

    # ============================================================================
    # SOURCE-SPECIFIC FIELDS
    # ============================================================================
    archive_url: Mapped[str | None] = mapped_column(
        String(1000), 
        nullable=True
    )
    
    downloads: Mapped[int] = mapped_column(
        Integer, 
        default=0, 
        nullable=False
    )
    
    num_reviews: Mapped[int] = mapped_column(
        Integer, 
        default=0, 
        nullable=False
    )

    # ============================================================================
    # TORRENT INFO
    # ============================================================================
    torrents: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )
    
    # Search keywords for better matching
    search_keywords: Mapped[list[str] | None] = mapped_column(
        ARRAY(String(100)),
        nullable=True,
        comment="Keywords for search optimization"
    )

    # ============================================================================
    # DOWNLOAD STATUS
    # ============================================================================
    downloaded: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True
    )
    
    download_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )
    
    download_progress: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    
    download_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    
    file_path: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )
    
    file_size: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )
    
    downloaded_quality: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    # ============================================================================
    # WATCH TRACKING
    # ============================================================================
    last_watched_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True
    )
    
    view_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    # ============================================================================
    # TIMESTAMPS
    # ============================================================================
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # ============================================================================
    # RELATIONSHIPS
    # ============================================================================
    genres: Mapped[list["Genre"]] = relationship(
        "Genre",
        secondary=movie_genres,
        back_populates="movies",
        lazy="selectin"
    )
    
    cast_members: Mapped[list["CastMember"]] = relationship(
        "CastMember",
        back_populates="movie",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    videos: Mapped[list["Video"]] = relationship(
        "Video",
        back_populates="movie",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    comment : Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="movie",
        cascade="all, delete-orphan",
        order_by="Comment.created_at.desc()"
    )
    
    watch_history: Mapped[list["WatchHistory"]] = relationship(
        "WatchHistory",
        back_populates="movie",
        cascade="all, delete-orphan"
    )
    
    subtitles: Mapped[list["Subtitle"]] = relationship(
        "Subtitle",
        back_populates="movie",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # ============================================================================
    # TABLE INDEXES
    # ============================================================================
    __table_args__ = (
        Index('ix_movies_cleanup', 'downloaded', 'last_watched_at'),
        Index('ix_movies_popular', 'popularity_score', 'is_popular'),
        Index('ix_movies_search', 'title', 'year', 'search_keywords'),
        Index('ix_movies_cache', 'metadata_fetched_at', 'source'),
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
    
    def increment_search_hits(self):
        """Increment search counter and update timestamp."""
        self.search_cache_hits += 1
        self.last_searched_at = datetime.utcnow()
    
    def is_metadata_stale(self) -> bool:
        """Check if metadata needs refresh."""
        if not self.metadata_fetched_at:
            return True
        
        days_since_fetch = (datetime.utcnow() - self.metadata_fetched_at).days
        return days_since_fetch > self.metadata_freshness_days
    
    def update_popularity_score(self):
        """Calculate and update popularity score."""
        # Base score from downloads
        base_score = self.downloads or 0
        
        # Boost from rating (if available)
        rating = self.archive_rating or self.imdb_rating or 0
        if rating > 0:
            # Normalize rating impact (0-5 star or 0-10 scale)
            rating_factor = rating / 5.0 if self.archive_rating else rating / 10.0
            base_score *= (1 + rating_factor)
        
        self.popularity_score = base_score
    
    def get_basic_info(self) -> dict:
        """Return basic movie info for search results."""
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "rating": self.archive_rating or self.imdb_rating,
            "cast": [c.name for c in self.cast_members] if self.cast_members else [],
            "genres": [g.name for g in self.genres] if self.genres else [],
            "poster_url": self.poster_url,
            "runtime": self.runtime,
            "source": self.source,
            "is_available": self.is_available(),
            "downloads": self.downloads,
        }
    
    def get_full_info(self) -> dict:
        """Return complete movie info."""
        basic = self.get_basic_info()
        basic.update({
            "description": self.description,
            "director": self.director,
            "language": self.language,
            "imdb_id": self.imdb_id,
            "archive_url": self.archive_url,
            "num_reviews": self.num_reviews,
            "torrents": self.torrents,
            "view_count": self.view_count,
            "last_watched_at": self.last_watched_at.isoformat() if self.last_watched_at else None,
            "metadata_fetched_at": self.metadata_fetched_at.isoformat() if self.metadata_fetched_at else None,
            "search_cache_hits": self.search_cache_hits,
            "popularity_rank": self.popularity_rank,
            "popularity_score": self.popularity_score,
            "is_popular": self.is_popular,
        })
        return basic