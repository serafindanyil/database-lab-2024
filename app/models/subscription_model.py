from app.extensions import db
from . import BaseModel


class Subscription(BaseModel):
    __tablename__ = "subscription"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan = db.Column(db.String(45), nullable=False, unique=True)
    price = db.Column(db.Integer, default=0, nullable=False)

    users = db.relationship("User", back_populates="subscription")
