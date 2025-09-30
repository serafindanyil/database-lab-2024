from sqlalchemy import select

from app.extensions import db
from app.models.download_model import Download
from app.models.user_model import User


class UserDao:
    def get_all(self):
        return db.session.scalars(select(User).order_by(User.id)).all()

    def get_by_id(self, user_id):
        return db.session.get(User, user_id)

    def create(self, data):
        """Просто створює об'єкт Python, не додаючи його до сесії."""
        new_user = User(**data)
        return new_user

    def update(self, user_id, data):
        user = self.get_by_id(user_id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        if not user:
            return False
        db.session.delete(user)
        return True

    def get_downloads(self):
        downloads = db.session.scalars(select(Download).order_by(Download.id)).all()
        return [
            {
                "id": download.id,
                "song_id": download.song_id,
                "user_id": download.user_id,
            }
            for download in downloads
        ]


user_dao = UserDao()
