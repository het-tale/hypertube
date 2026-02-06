# app/models/__init__.py

"""Models package - imports all models for SQLAlchemy."""

# Import Base first
from app.db.session import Base

# Import all models in order (parent models first)
from app.models.models import User, RefreshToken, OAuthAccount
from app.models.comment import Comment
from app.models.watch_history import WatchHistory
from app.models.movie import Movie
# ... import other models

__all__ = [
    "Base",
    "User",
    "RefreshToken",
    "OAuthAccount",
    "Comment",
    "WatchHistory",
    "Movie",
]