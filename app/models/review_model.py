from app.extensions import db
from . import BaseModel


class Review(BaseModel):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey("song.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    song = db.relationship("Song", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")
