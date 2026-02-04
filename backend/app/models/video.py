from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum as SQLEnum,
)
from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.security import utcnow

if TYPE_CHECKING:
    from app.models.movie import Movie

from enum import Enum


class StatusType(str, Enum):
    """Enum for video download status"""

    DOWNLOADING = "downloading"
    CONVERTING = "converting"
    READY = "ready"
    ERROR = "error"


class Video(Base):
    """Video model"""

    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("movies.id", ondelete="CASCADE"),
        index=True,
        unique=True,
        nullable=False,
    )
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    original_format: Mapped[str | None] = mapped_column(String(10))
    converted_format: Mapped[str | None] = mapped_column(String(10))
    file_size: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    duration: Mapped[int | None] = mapped_column(Integer, nullable=True)
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(
        SQLEnum(StatusType, native_enum=False, length=20),
        nullable=False,
        default=StatusType.DOWNLOADING,
    )
    downloaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_watched_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=utcnow, onupdate=utcnow
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, nullable=False
    )
    movie: Mapped["Movie"] = relationship("Movie", back_populates="video")

    __table_args__ = (
        CheckConstraint(
            "progress >= 0 AND progress <= 100", name="check_progress_range"
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<Video(id={self.id}, movie_id='{self.movie_id}', status='{self.status}')>"
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "movie_id": self.movie_id,
            "file_path": self.file_path,
            "original_format": self.original_format,
            "converted_format": self.converted_format,
            "file_size": self.file_size,
            "duration": self.duration,
            "status": self.status,
            "progress": self.progress,
            "downloaded_at": (
                self.downloaded_at.isoformat() if self.downloaded_at else None
            ),
            "last_watched_at": (
                self.last_watched_at.isoformat() if self.last_watched_at else None
            ),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @property
    def is_streamable(self) -> bool:
        """Check if video has enough data to start streaming"""
        return self.status == StatusType.READY or (
            self.status == StatusType.DOWNLOADING and self.progress >= 10
        )

    @property
    def is_complete(self) -> bool:
        """Check if download is 100% complete"""
        return self.progress == 100 and self.status != StatusType.ERROR
