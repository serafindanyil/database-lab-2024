from sqlalchemy import text
from app import db

class creator_dao:
    @staticmethod
    def get_all():
        query = text("SELECT * FROM Creator")
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_by_id(creator_id):
        query = text("SELECT * FROM Creator WHERE ID = :id")
        result = db.session.execute(query, {'id': creator_id}).mappings().first()
        return dict(result) if result else None

    @staticmethod
    def create(data):
        db.session.execute(text("""
            INSERT INTO Creator (release_date, Authorization_ID, name, Label_ID, Profile_creator_ID)
            VALUES (:release_date, :authorization_id, :name, :label_id, :profile_creator_id)
        """), data)
        db.session.commit()
        result = db.session.execute(text("SELECT LAST_INSERT_ID() AS ID"))
        new_id = result.fetchone()['ID']
        return {"ID": new_id, **data}

    @staticmethod
    def update(creator_id, data):
        db.session.execute(text("""
            UPDATE Creator SET release_date = :release_date, Authorization_ID = :authorization_id,
            name = :name, Label_ID = :label_id, Profile_creator_ID = :profile_creator_id
            WHERE ID = :id
        """), {**data, 'id': creator_id})
        db.session.commit()
        return creator_dao.get_by_id(creator_id)

    @staticmethod
    def delete(creator_id):
        result = db.session.execute(text("DELETE FROM Creator WHERE ID = :id"), {'id': creator_id})
        db.session.commit()
        return result.rowcount > 0
