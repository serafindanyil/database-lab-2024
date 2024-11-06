from sqlalchemy import text
from app import db

class GenreDAO:
    @staticmethod
    def get_all():
        query = text("SELECT * FROM Genre")
        result = db.session.execute(query).mappings().all()  # Використовуємо .mappings()
        return [dict(row) for row in result]

    @staticmethod
    def get_by_id(genre_id):
        query = text("SELECT * FROM Genre WHERE id = :id")
        result = db.session.execute(query, {'id': genre_id}).mappings().first()  # Використовуємо .mappings()
        return dict(result) if result else None


    @staticmethod
    def create(data):
        db.session.execute(text("INSERT INTO Genre (name) VALUES (:name)"), {'name': data['name']})
        db.session.commit()
        result = db.session.execute(text("SELECT LAST_INSERT_ID() AS ID"))
        new_id = result.fetchone()['ID']
        return {"ID": new_id, "name": data['name']}

    @staticmethod
    def update(genre_id, data):
        db.session.execute(text("UPDATE Genre SET name = :name WHERE ID = :id"), {'name': data['name'], 'id': genre_id})
        db.session.commit()
        return GenreDAO.get_by_id(genre_id)

    @staticmethod
    def delete(genre_id):
        result = db.session.execute(text("DELETE FROM Genre WHERE ID = :id"), {'id': genre_id})
        db.session.commit()
        return result.rowcount > 0
