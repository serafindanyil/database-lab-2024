from app import db
from sqlalchemy import text

class album_dao:
    @staticmethod
    def get_all():
        query = text("SELECT * FROM Album")
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_by_id(album_id):
        query = text("SELECT * FROM Album WHERE ID = :id")
        result = db.session.execute(query, {'id': album_id}).mappings().first()
        return dict(result) if result else None

    @staticmethod
    def create(data):
        db.session.execute(text("""
            INSERT INTO Album (name, release_date, Creator_ID, Creator_Profile_creator_ID)
            VALUES (:name, :release_date, :creator_id, :creator_profile_creator_id)
        """), data)
        db.session.commit()
        result = db.session.execute(text("SELECT LAST_INSERT_ID() AS ID"))
        new_id = result.fetchone()['ID']
        return {"ID": new_id, **data}

    @staticmethod
    def update(album_id, data):
        db.session.execute(text("""
            UPDATE Album SET name = :name, release_date = :release_date,
            Creator_ID = :creator_id, Creator_Profile_creator_ID = :creator_profile_creator_id
            WHERE ID = :id
        """), {**data, 'id': album_id})
        db.session.commit()
        return album_dao.get_by_id(album_id)

    @staticmethod
    def delete(album_id):
        result = db.session.execute(text("DELETE FROM Album WHERE ID = :id"), {'id': album_id})
        db.session.commit()
        return result.rowcount > 0
