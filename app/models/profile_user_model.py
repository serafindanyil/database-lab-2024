from app.extensions import db
from . import BaseModel


class ProfileUser(BaseModel):
    __tablename__ = "profile_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_link = db.Column(db.String(150))
    bio = db.Column(db.String(500))

    user = db.relationship("User", back_populates="profile_user", uselist=False)
