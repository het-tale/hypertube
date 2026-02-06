# app/models/genre.py

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


if TYPE_CHECKING:
    from app.models.movie import Movie

# Many-to-Many association table
movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", String(255), ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)


class Genre(Base):
    """Genre model"""
    
    __tablename__ = "genres"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    # Example: "Action", "Comedy", "Drama"
    
    # Many-to-Many relationship
    movies: Mapped[list["Movie"]] = relationship(
        "Movie",
        secondary=movie_genres,
        back_populates="genres"  # Note: different name to avoid conflict
    )
    
    def __repr__(self):
        return f"<Genre(name='{self.name}')>"