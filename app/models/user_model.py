from app.extensions import db
from . import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)

    # ЗМІНЕНО: Імена колонок та зовнішніх ключів
    authorization_id = db.Column(
        db.Integer, db.ForeignKey("authorization.id"), nullable=False
    )
    profile_user_id = db.Column(
        db.Integer, db.ForeignKey("profile_user.id"), nullable=False
    )
    subscription_id = db.Column(
        db.Integer, db.ForeignKey("subscription.id"), nullable=False
    )

    authorization = db.relationship("Authorization", back_populates="users")
    profile_user = db.relationship(
        "ProfileUser",
        back_populates="user",
        uselist=False,
        foreign_keys=[profile_user_id],
    )
    subscription = db.relationship("Subscription", back_populates="users")
    downloads = db.relationship(
        "Download", back_populates="user", cascade="all, delete-orphan"
    )
    reviews = db.relationship(
        "Review", back_populates="user", cascade="all, delete-orphan"
    )

    def to_dict(self):
        profile = self.profile_user.to_dict() if self.profile_user else None
        subscription = self.subscription.to_dict() if self.subscription else None
        return {
            "id": self.id,
            "name": self.name,
            "authorization_id": self.authorization_id,
            "profile_user_id": self.profile_user_id,
            "subscription_id": self.subscription_id,
            "profile": profile,
            "subscription": subscription,
        }
