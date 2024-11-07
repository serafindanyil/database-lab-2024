from sqlalchemy import text
from app import db

class song_dao:
    @staticmethod
    def get_all():
        query = text("SELECT * FROM Song")
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_by_id(song_id):
        query = text("SELECT * FROM Song WHERE ID = :id")
        result = db.session.execute(query, {'id': song_id}).mappings().first()
        return dict(result) if result else None

    @staticmethod
    def create(data):
        db.session.execute(text("INSERT INTO Song (name, Genre_ID, download_count) VALUES (:name, :genre_id, :download_count)"),
                           {'name': data['name'], 'genre_id': data['Genre_ID'], 'download_count': data.get('download_count', 0)})
        db.session.commit()
        result = db.session.execute(text("SELECT LAST_INSERT_ID() AS ID"))
        new_id = result.fetchone()['ID']
        return {"ID": new_id, **data}

    @staticmethod
    def update(song_id, data):
        db.session.execute(text("UPDATE Song SET name = :name, Genre_ID = :genre_id, download_count = :download_count WHERE ID = :id"),
                           {'name': data['name'], 'genre_id': data['Genre_ID'], 'download_count': data['download_count'], 'id': song_id})
        db.session.commit()
        return song_dao.get_by_id(song_id)

    @staticmethod
    def delete(song_id):
        result = db.session.execute(text("DELETE FROM Song WHERE ID = :id"), {'id': song_id})
        db.session.commit()
        return result.rowcount > 0
