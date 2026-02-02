"""Database models."""
from datetime import datetime
# from enum import Enum as PyEnum

from app.movies.schemas import MediaType
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.security import utcnow
from app.db.session import Base
from app.models.association_tables import media_genres


class User(Base):
    """User model for authentication."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, onupdate=utcnow, nullable=False
    )

    # Relationships
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )


class RefreshToken(Base):
    """Refresh token model for stateful token management with rotation."""

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token: Mapped[str] = mapped_column(Text, unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")



class Movie(Base):

    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title : Mapped[str]  = mapped_column(String(255), unique=True, index=True)
    media_type : Mapped[MediaType] = mapped_column(Enum(MediaType))
    description: Mapped[str | None] = mapped_column(Text)
    release_year: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Type-specific fields
    runtime_minutes: Mapped[int | None]  # Movies
    num_seasons: Mapped[int | None]  # TV shows
    
    # Relationships
    genres: Mapped[list["Genre"]] = relationship(
        secondary=media_genres,
        back_populates="media_items"
    )

# class Actors(Base):


# class WatchList(Base):

class Genre(Base):
    __tablename__ = "genres"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    
    # Reverse relationship
    media_items: Mapped[list["Movie"]] = relationship(
        secondary=media_genres,
        back_populates="genres"
    )
    
    def __repr__(self):
        return f"<Genre(name='{self.name}')>"
