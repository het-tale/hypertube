from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    Boolean,
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
    from app.models.models import User


class WatchHistory(Base):
    """Watch History Model"""

    __tablename__ = "watch_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    movie_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("movies.id", ondelete="CASCADE"),
        index=True,
        unique=True,
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        unique=True,
        nullable=False,
    )
    watched_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, index=True)
    watch_duration: Mapped[int] = mapped_column(Integer)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    movie: Mapped["Movie"] = relationship("Movie", back_populates="watch_history")
    user: Mapped["User"] = relationship("User", back_populates="watch_history")

    __table_args__ = UniqueConstraint("movie_id", "user_id", name="movie_user_uc")

    def __repr__(self) -> str:
        return f"<Watch History(id={self.id}, movie_id='{self.movie_id}', watched_at='{self.watched_at}')>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "movie_id": self.movie_id,
            "user_id": self.user_id,
            "watched_at": self.watched_at,
            "watch_duration": self.watch_duration,
            "completed": self.completed,
        }
