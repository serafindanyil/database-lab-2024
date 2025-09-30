from app.extensions import db
from app.models.profile_user_model import ProfileUser


class ProfileUserDao:
    def create(self, data=None):
        payload = data or {}
        new_profile = ProfileUser(
            picture_link=payload.get("picture_link"),
            bio=payload.get("bio"),
        )
        db.session.add(new_profile)
        return new_profile


# Створюємо єдиний екземпляр
profile_user_dao = ProfileUserDao()
