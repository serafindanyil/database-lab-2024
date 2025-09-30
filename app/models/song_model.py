from app.extensions import db


class Song(db.Model):
    __tablename__ = "song"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    genre_name = db.Column(db.String(45), db.ForeignKey("genre.name"), nullable=False)
    link = db.Column(db.String(45), nullable=False)
    download_count = db.Column(db.Integer, default=0)

    # ЗМІНЕНО: Додано зворотні зв'язки для повноцінної роботи relationships
    genre = db.relationship("Genre", back_populates="songs")
    downloads = db.relationship("Download", back_populates="song")
    song_creators = db.relationship("SongHasCreator", back_populates="song")
    song_albums = db.relationship("SongHasAlbum", back_populates="song")
    reviews = db.relationship("Review", back_populates="song", cascade="all, delete-orphan")
