from sqlalchemy import text
from app import db
class subcription_dao:
    @staticmethod
    def get_all():
        query = text("SELECT * FROM Subcription")
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_by_id(subcription_id):
        query = text("SELECT * FROM Subcription WHERE ID = :id")
        result = db.session.execute(query, {'id': subcription_id}).mappings().first()
        return dict(result) if result else None

    @staticmethod
    def create(data):
        db.session.execute(text("INSERT INTO Subcription (plan, price) VALUES (:plan, :price)"), data)
        db.session.commit()
        result = db.session.execute(text("SELECT LAST_INSERT_ID() AS ID"))
        new_id = result.fetchone()['ID']
        return {"ID": new_id, **data}

    @staticmethod
    def update(subcription_id, data):
        db.session.execute(text("""
            UPDATE Subcription SET plan = :plan, price = :price WHERE ID = :id
        """), {**data, 'id': subcription_id})
        db.session.commit()
        return subcription_dao.get_by_id(subcription_id)

    @staticmethod
    def delete(subcription_id):
        result = db.session.execute(text("DELETE FROM Subcription WHERE ID = :id"), {'id': subcription_id})
        db.session.commit()
        return result.rowcount > 0
