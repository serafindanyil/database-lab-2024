from app.extensions import db


class SongHasCreator(db.Model):
    __tablename__ = "song_has_creator"

    song_id = db.Column(db.Integer, db.ForeignKey("song.id"), primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("creator.id"), primary_key=True)

    song = db.relationship("Song", back_populates="song_creators")
    creator = db.relationship("Creator", back_populates="song_creators")
