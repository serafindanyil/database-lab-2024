from app import db
from sqlalchemy import text


class authorization_dao:
    @staticmethod
    def get_all():
        query = text("SELECT * FROM Authorization")
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_by_id(auth_id):
        query = text("SELECT * FROM Authorization WHERE ID = :id")
        result = db.session.execute(query, {'id': auth_id}).mappings().first()
        return dict(result) if result else None

    @staticmethod
    def create(data):
        db.session.execute(text("INSERT INTO Authorization (email, password) VALUES (:email, :password)"),
                           {'email': data['email'], 'password': data['password']})
        db.session.commit()
        result = db.session.execute(text("SELECT LAST_INSERT_ID() AS ID"))
        new_id = result.fetchone()['ID']
        return {"ID": new_id, **data}

    @staticmethod
    def update(auth_id, data):
        db.session.execute(text("UPDATE Authorization SET email = :email, password = :password WHERE ID = :id"),
                           {'email': data['email'], 'password': data['password'], 'id': auth_id})
        db.session.commit()
        return authorization_dao.get_by_id(auth_id)

    @staticmethod
    def delete(auth_id):
        result = db.session.execute(text("DELETE FROM Authorization WHERE ID = :id"), {'id': auth_id})
        db.session.commit()
        return result.rowcount > 0
