from app.extensions import db
from . import BaseModel


class Authorization(BaseModel):
    __tablename__ = "authorization"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(24), nullable=False)
    users = db.relationship(
        "User",
        back_populates="authorization",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    creators = db.relationship(
        "Creator",
        back_populates="authorization",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
