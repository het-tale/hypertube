from typing import TYPE_CHECKING
from sqlalchemy import String
from app.db.session import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column

if TYPE_CHECKING:
    from app.models.cast import Cast
    from app.models.comment import Comment
    from app.models.subtitle import Subtitle
    from app.models.watch_history import WatchHistory
    from app.models.video import Video


class Movie(Base):
    __tablename__ = "movies"
    # other fields
    id: Mapped[str] = mapped_column(String, primary_key=True)
    # Relationships
    cast: Mapped[list["Cast"]] = relationship(
        "Cast",
        back_populates="movie",
        cascade="all, delete-orphan",
    )
    video: Mapped["Video"] = relationship(
        "Video", back_populates="movie", cascade="all, delete-orphan"
    )
    comment: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="movie",
        cascade="all, delete-orphan",
    )
    watch_history: Mapped[list["WatchHistory"]] = relationship(
        "WatchHistory",
        back_populates="movie",
        cascade="all, delete-orphan",
    )
    subtitle: Mapped[list["Subtitle"]] = relationship(
        "Subtitle",
        back_populates="movie",
        cascade="all, delete-orphan",
    )
