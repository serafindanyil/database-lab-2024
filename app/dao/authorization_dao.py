from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.authorization_model import Authorization

class AuthorizationDAO:
    def get_all(self):
        return Authorization.query.order_by(Authorization.id).all()

    def get_by_id(self, auth_id):
        return db.session.get(Authorization, auth_id)

    def create(self, data):
        try:
            new_auth = Authorization(**data)
            db.session.add(new_auth)
            db.session.commit()
            return new_auth
        except IntegrityError as exc:
            db.session.rollback()
            raise ValueError("Email already exists") from exc

    def update(self, auth_id, data):
        auth = self.get_by_id(auth_id)
        if not auth:
            return None
        for key, value in data.items():
            setattr(auth, key, value)
        db.session.commit()
        return auth

    def delete(self, auth_id):
        auth = self.get_by_id(auth_id)
        if not auth:
            return False
        db.session.delete(auth)
        db.session.commit()
        return True

authorization_dao = AuthorizationDAO()