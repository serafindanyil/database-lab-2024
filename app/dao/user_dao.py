from app import db
from sqlalchemy import text

class user_dao:
    @staticmethod
    def get_all():
        query = text("SELECT * FROM User")
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_by_id(user_id):
        query = text("SELECT * FROM User WHERE ID = :id")
        result = db.session.execute(query, {'id': user_id}).mappings().first()
        return dict(result) if result else None

    @staticmethod
    def create(data):
        db.session.execute(text("""
            INSERT INTO User (name, Authorization_ID, Profile_user_ID, Subcription_ID)
            VALUES (:name, :authorization_id, :profile_user_id, :subcription_id)
        """), data)
        db.session.commit()
        result = db.session.execute(text("SELECT LAST_INSERT_ID() AS ID"))
        new_id = result.fetchone()['ID']
        return {"ID": new_id, **data}

    @staticmethod
    def update(user_id, data):
        db.session.execute(text("""
            UPDATE User SET name = :name, Authorization_ID = :authorization_id,
            Profile_user_ID = :profile_user_id, Subcription_ID = :subcription_id WHERE ID = :id
        """), {**data, 'id': user_id})
        db.session.commit()
        return user_dao.get_by_id(user_id)

    @staticmethod
    def delete(user_id):
        result = db.session.execute(text("DELETE FROM User WHERE ID = :id"), {'id': user_id})
        db.session.commit()
        return result.rowcount > 0
