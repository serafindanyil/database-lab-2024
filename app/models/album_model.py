from app.extensions import db


class Album(db.Model):
    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)

    # ЗМІНЕНО: Імена колонок та зовнішніх ключів
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'), nullable=False)

    # ВИДАЛЕНО: Ця колонка була зайвою, оскільки зв'язок з профілем
    # творця вже встановлено через модель Creator.
    # Creator_Profile_creator_ID = db.Column(db.Integer, nullable=False)

    creator = db.relationship('Creator', back_populates='albums')
    song_albums = db.relationship('SongHasAlbum', back_populates='album')