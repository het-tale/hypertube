from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.movie import Movie
from app.models.comment import Comment


class MovieService:
    async def get_movie(self, movie_id: str, db: AsyncSession = Depends(get_db)):
        statement = (
            select(Movie)
            .options(
                selectinload(Movie.cast),
                selectinload(Movie.video),
                selectinload(Movie.comment).selectinload(Comment.user),
            )
            .where(Movie.id == movie_id)
        )
        result = await db.execute(statement)
        movie = result.scalar_one_or_none()
        return movie


movie_service = MovieService()
