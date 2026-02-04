from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.security import utcnow

if TYPE_CHECKING:
    from app.models.movie import Movie


class Subtitle(Base):
    """Subtitles model"""

    __tablename__ = "subtitles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("movies.id", ondelete="CASCADE"),
        index=True,
        unique=True,
        nullable=False,
    )
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    language_name: Mapped[str] = mapped_column(String(50))
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    source: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, nullable=False
    )
    movie: Mapped["Movie"] = relationship("Movie", back_populates="subtitle")

    __table_args__ = UniqueConstraint("movie_id", "language", name="movie_language_uc")

    def __repr__(self) -> str:
        return f"<Subtitle(id={self.id}, movie_id='{self.movie_id}', language='{self.language}')>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "movie_id": self.movie_id,
            "language": self.language,
            "language_name": self.language_name,
            "file_path": self.file_path,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
