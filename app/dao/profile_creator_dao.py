from app import db
from sqlalchemy import text

class profile_creator_dao:
    @staticmethod
    def get_all():
        query = text("SELECT * FROM Profile_creator")
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_by_id(profile_id):
        query = text("SELECT * FROM Profile_creator WHERE ID = :id")
        result = db.session.execute(query, {'id': profile_id}).mappings().first()
        return dict(result) if result else None

    @staticmethod
    def create(data):
        db.session.execute(text("INSERT INTO Profile_creator (user_ID, picture_link, bio) VALUES (:user_id, :picture_link, :bio)"),
                           {'user_id': data['user_ID'], 'picture_link': data.get('picture_link'), 'bio': data.get('bio')})
        db.session.commit()
        result = db.session.execute(text("SELECT LAST_INSERT_ID() AS ID"))
        new_id = result.fetchone()['ID']
        return {"ID": new_id, **data}

    @staticmethod
    def update(profile_id, data):
        db.session.execute(text("UPDATE Profile_creator SET user_ID = :user_id, picture_link = :picture_link, bio = :bio WHERE ID = :id"),
                           {'user_id': data['user_ID'], 'picture_link': data['picture_link'], 'bio': data['bio'], 'id': profile_id})
        db.session.commit()
        return profile_creator_dao.get_by_id(profile_id)

    @staticmethod
    def delete(profile_id):
        result = db.session.execute(text("DELETE FROM Profile_creator WHERE ID = :id"), {'id': profile_id})
        db.session.commit()
        return result.rowcount > 0
