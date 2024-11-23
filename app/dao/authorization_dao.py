from app import db
from sqlalchemy import text


class authorization_dao:
    @staticmethod
    def get_all():
        query = text("SELECT * FROM authorization")
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_by_id(auth_id):
        query = text("SELECT * FROM authorization WHERE ID = :id")
        result = db.session.execute(query, {'id': auth_id}).mappings().first()
        return dict(result) if result else None

    @staticmethod
    def create(data):
        db.session.execute(
            text("INSERT INTO authorization (email, password) VALUES (:email, :password)"),
            {'email': data['email'], 'password': data['password']}
        )
        db.session.commit()

        result = db.session.execute(text("SELECT LAST_INSERT_ID() AS ID")).mappings().first()
        if result is None:
            raise ValueError("LAST_INSERT_ID() did not return any value")
        new_id = result['ID']
        return {"ID": new_id, **data}

    @staticmethod
    def update(auth_id, data):
        db.session.execute(text("UPDATE authorization SET email = :email, password = :password WHERE ID = :id"),
                           {'email': data['email'], 'password': data['password'], 'id': auth_id})
        db.session.commit()
        return authorization_dao.get_by_id(auth_id)

    @staticmethod
    def delete(auth_id):
        try:
            # Видалення пов'язаних записів із song_has_album через album
            db.session.execute(
                text("""
                DELETE song_has_album 
                FROM song_has_album
                JOIN album ON song_has_album.album_creator_authorization_id = album.creator_authorization_id
                WHERE album.creator_authorization_id = :auth_id
                """),
                {'auth_id': auth_id}
            )

            # Видалення пов'язаних записів з album
            db.session.execute(
                text("DELETE FROM album WHERE creator_authorization_id = :auth_id"),
                {'auth_id': auth_id}
            )

            # Видалення запису з authorization
            result = db.session.execute(
                text("DELETE FROM authorization WHERE ID = :id"),
                {'id': auth_id}
            )

            db.session.commit()
            return result.rowcount > 0

        except Exception as e:
            db.session.rollback()  # Відміняємо зміни в разі помилки
            raise e  # Піднімаємо помилку для подальшої обробки
