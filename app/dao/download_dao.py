from sqlalchemy import text
from app import db


class download_dao:
    @staticmethod
    def get_all():
        query = text("SELECT * FROM Download")
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_by_id(download_id):
        query = text("SELECT * FROM Download WHERE ID = :id")
        result = db.session.execute(query, {'id': download_id}).mappings().first()
        return dict(result) if result else None

    @staticmethod
    def create(data):
        db.session.execute(text("""
            INSERT INTO Download (Song_ID, User_ID)
            VALUES (:song_id, :user_id)
        """), data)
        db.session.commit()
        result = db.session.execute(text("SELECT LAST_INSERT_ID() AS ID"))
        new_id = result.fetchone()['ID']
        return {"ID": new_id, **data}

    @staticmethod
    def delete(download_id):
        result = db.session.execute(text("DELETE FROM Download WHERE ID = :id"), {'id': download_id})
        db.session.commit()
        return result.rowcount > 0
