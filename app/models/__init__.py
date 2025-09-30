# /app/models/__init__.py
from app.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Тепер імпортуйте всі ваші моделі
from .genre_model import Genre
from .song_model import Song
from .authorization_model import Authorization
from .label_model import Label
from .profile_creator_model import ProfileCreator
from .creator_model import Creator
from .album_model import Album
from .profile_user_model import ProfileUser
from .subscription_model import Subscription
from .user_model import User
from .download_model import Download
from .song_has_creator_model import SongHasCreator
from .song_has_album_model import SongHasAlbum
from .review_model import Review

__all__ = [
    "BaseModel",
    "Genre",
    "Song",
    "Authorization",
    "Label",
    "ProfileCreator",
    "Creator",
    "Album",
    "ProfileUser",
    "Subscription",
    "User",
    "Download",
    "SongHasCreator",
    "SongHasAlbum",
    "Review",
]
