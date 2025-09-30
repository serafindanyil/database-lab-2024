from app.extensions import db
from . import BaseModel


class Genre(BaseModel):
    __tablename__ = 'genre'

    name = db.Column(db.String(45), primary_key=True)

    # ЗМІНЕНО: Замінено backref на більш явний back_populates
    songs = db.relationship('Song', back_populates='genre')