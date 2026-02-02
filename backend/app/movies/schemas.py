from enum import Enum as PyEnum


class MediaType(PyEnum):
    """Enum for media types."""
    MOVIE = "movie"
    TV_SHOW = "tv_show"
    DOCUMENTARY = "documentary"
    SHORT_FILM = "short_film"
