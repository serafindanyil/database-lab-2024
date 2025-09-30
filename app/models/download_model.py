from app.extensions import db
from . import BaseModel


class Download(BaseModel):
    __tablename__ = 'download'

    id = db.Column(db.Integer, primary_key=True)

    # ЗМІНЕНО: Імена колонок та зовнішніх ключів
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    song = db.relationship('Song', back_populates='downloads')
    user = db.relationship('User', back_populates='downloads')