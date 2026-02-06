from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, String, Enum as SQLEnum
from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.security import utcnow

if TYPE_CHECKING:
    from app.models.movie import Movie

from enum import Enum


class RoleType(str, Enum):
    """Enum for cast member roles"""

    DIRECTOR = "director"
    ACTOR = "actor"
    PRODUCER = "producer"
    WRITER = "writer"


class CastMember(Base):
    """Cast model"""

    __tablename__ = "cast_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("movies.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(
        SQLEnum(RoleType, native_enum=False, max=20), nullable=False
    )

    character: Mapped[str | None] = mapped_column(String(100), nullable=True)
    display_order: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, nullable=False
    )
    movie: Mapped["Movie"] = relationship("Movie", back_populates="cast_members")

    def __repr__(self):
        """String representation for debugging"""
        return f"<Cast(id={self.id}, name='{self.name}', role='{self.role}')>"

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "movie_id": self.movie_id,
            "name": self.name,
            "role": self.role,
            "character": self.character,
            "order": self.display_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
