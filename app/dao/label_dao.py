from app import db
from sqlalchemy import text

class label_dao:
    @staticmethod
    def get_all():
        query = text("SELECT * FROM Label")
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_by_id(label_id):
        query = text("SELECT * FROM Label WHERE ID = :id")
        result = db.session.execute(query, {'id': label_id}).mappings().first()
        return dict(result) if result else None

    @staticmethod
    def create(data):
        db.session.execute(text("INSERT INTO Label (name) VALUES (:name)"), {'name': data['name']})
        db.session.commit()
        result = db.session.execute(text("SELECT LAST_INSERT_ID() AS ID"))
        new_id = result.fetchone()['ID']
        return {"ID": new_id, "name": data['name']}

    @staticmethod
    def update(label_id, data):
        db.session.execute(text("UPDATE Label SET name = :name WHERE ID = :id"), {'name': data['name'], 'id': label_id})
        db.session.commit()
        return label_dao.get_by_id(label_id)

    @staticmethod
    def delete(label_id):
        result = db.session.execute(text("DELETE FROM Label WHERE ID = :id"), {'id': label_id})
        db.session.commit()
        return result.rowcount > 0
