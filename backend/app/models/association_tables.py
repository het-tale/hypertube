"""Association/junction tables for many-to-many relationships."""
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.session import Base
from datetime import datetime


# Media <-> Genres
media_genres = Table(
    "media_genres",
    Base.metadata,
    Column("media_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)


# Media <-> Actors (if you add actors later)
# media_actors = Table(
#     "media_actors",
#     Base.metadata,
#     Column("media_id", Integer, ForeignKey("media.id", ondelete="CASCADE"), primary_key=True),
#     Column("actor_id", Integer, ForeignKey("actors.id", ondelete="CASCADE"), primary_key=True),
# )


# # User <-> Media (watchlist many-to-many)
# user_watchlist = Table(
#     "user_watchlist",
#     Base.metadata,
#     Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
#     Column("media_id", Integer, ForeignKey("media.id", ondelete="CASCADE"), primary_key=True),
#     Column("added_at", Integer, default=lambda: int(datetime.utcnow().timestamp())),
# )