from sqlalchemy import text
from app import db

class song_has_creator_dao:
    @staticmethod
    def create(song_id, creator_id):
        db.session.execute(text("INSERT INTO Song_has_Creator (Song_ID, Creator_ID) VALUES (:song_id, :creator_id)"),
                           {'song_id': song_id, 'creator_id': creator_id})
        db.session.commit()

    @staticmethod
    def delete(song_id, creator_id):
        result = db.session.execute(text("DELETE FROM Song_has_Creator WHERE Song_ID = :song_id AND Creator_ID = :creator_id"),
                                    {'song_id': song_id, 'creator_id': creator_id})
        db.session.commit()
        return result.rowcount > 0
