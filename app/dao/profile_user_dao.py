from app import db
from sqlalchemy import text

class profile_user_dao:
    @staticmethod
    def get_all():
        query = text("SELECT * FROM Profile_user")
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_by_id(profile_id):
        query = text("SELECT * FROM Profile_user WHERE ID = :id")
        result = db.session.execute(query, {'id': profile_id}).mappings().first()
        return dict(result) if result else None

    @staticmethod
    def create(data):
        db.session.execute(text("""
            INSERT INTO Profile_user (user_ID, picture_link, bio)
            VALUES (:user_id, :picture_link, :bio)
        """), data)
        db.session.commit()
        result = db.session.execute(text("SELECT LAST_INSERT_ID() AS ID"))
        new_id = result.fetchone()['ID']
        return {"ID": new_id, **data}

    @staticmethod
    def update(profile_id, data):
        db.session.execute(text("""
            UPDATE Profile_user SET user_ID = :user_id, picture_link = :picture_link, bio = :bio
            WHERE ID = :id
        """), {**data, 'id': profile_id})
        db.session.commit()
        return profile_user_dao.get_by_id(profile_id)

    @staticmethod
    def delete(profile_id):
        result = db.session.execute(text("DELETE FROM Profile_user WHERE ID = :id"), {'id': profile_id})
        db.session.commit()
        return result.rowcount > 0
