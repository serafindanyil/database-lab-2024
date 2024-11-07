from app import db
from sqlalchemy import text

class song_has_album_dao:
    @staticmethod
    def create(song_id, album_id):
        db.session.execute(text("INSERT INTO Song_has_Album (Song_ID, Album_ID) VALUES (:song_id, :album_id)"),
                           {'song_id': song_id, 'album_id': album_id})
        db.session.commit()

    @staticmethod
    def delete(song_id, album_id):
        result = db.session.execute(text("DELETE FROM Song_has_Album WHERE Song_ID = :song_id AND Album_ID = :album_id"),
                                    {'song_id': song_id, 'album_id': album_id})
        db.session.commit()
        return result.rowcount > 0
