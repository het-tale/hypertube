from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    TEXT,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.security import utcnow

if TYPE_CHECKING:
    from app.models.movie import Movie
    from app.models.models import User


class Comment(Base):
    """Model for Comments"""

    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
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
    content: Mapped[int] = mapped_column(TEXT, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, onupdate=utcnow
    )
    movie: Mapped["Movie"] = relationship("Movie", back_populates="comment")
    user: Mapped["User"] = relationship("User", back_populates="comment")

    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, movie_id='{self.movie_id}', content='{self.content}')>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "movie_id": self.movie_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
