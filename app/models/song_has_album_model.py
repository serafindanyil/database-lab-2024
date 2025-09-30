from app.extensions import db

class SongHasAlbum(db.Model):
    __tablename__ = 'song_has_album'

    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), primary_key=True)

    song = db.relationship('Song', back_populates='song_albums')
    album = db.relationship('Album', back_populates='song_albums')