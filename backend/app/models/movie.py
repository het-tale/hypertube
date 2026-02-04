from app.db.session import Base
from sqlalchemy.orm import Mapped, relationship

from app.models.cast import Cast
from app.models.comment import Comment
from app.models.subtitle import Subtitle
from app.models.watch_history import WatchHistory
from app.models.video import Video


class Movie(Base):
    __tablename__ = "movies"
    # other fields

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
    watch_history: Mapped[list["Subtitle"]] = relationship(
        "Subtitle",
        back_populates="movie",
        cascade="all, delete-orphan",
    )
