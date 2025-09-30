from app.dao.profile_user_dao import profile_user_dao
from app.dao.user_dao import user_dao
from app.extensions import db
from app.models.authorization_model import Authorization
from app.models.subscription_model import Subscription


class UserService:
    @staticmethod
    def create_user(data):
        required_fields = {"name", "authorization_id", "subscription_id"}
        missing = required_fields - data.keys()
        if missing:
            field_list = ", ".join(sorted(missing))
            raise ValueError(f"Missing required fields: {field_list}")

        authorization = db.session.get(Authorization, data["authorization_id"])
        if authorization is None:
            raise ValueError("Authorization not found")

        subscription = db.session.get(Subscription, data["subscription_id"])
        if subscription is None:
            raise ValueError("Subscription not found")

        try:
            new_profile = profile_user_dao.create()
            db.session.flush()

            user_payload = {
                "name": data["name"],
                "authorization_id": authorization.id,
                "subscription_id": subscription.id,
                "profile_user_id": new_profile.id,
            }

            new_user = user_dao.create(user_payload)
            new_user.profile_user = new_profile
            db.session.add(new_user)
            db.session.commit()

            return new_user
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def get_all_users():
        return user_dao.get_all()

    @staticmethod
    def get_user_by_id(user_id):
        return user_dao.get_by_id(user_id)

    @staticmethod
    def get_downloads():
        return user_dao.get_downloads()

    @staticmethod
    def update_user(user_id, data):
        user = user_dao.get_by_id(user_id)
        if user is None:
            return None

        if "subscription_id" in data:
            subscription = db.session.get(Subscription, data["subscription_id"])
            if subscription is None:
                raise ValueError("Subscription not found")

        updated_user = user_dao.update(user_id, data)
        db.session.commit()
        return updated_user

    @staticmethod
    def delete_user(user_id):
        user_exists = user_dao.delete(user_id)
        if not user_exists:
            return False
        db.session.commit()
        return True
