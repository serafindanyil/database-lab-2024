from app import db
from sqlalchemy import text


class label_dao:
    @staticmethod
    def get_creator_for_every_label():
        # Оновлений SQL запит без коментарів
        query = text("""
        SELECT
            l.name AS label_name,
            c.name AS creator_name,
            GROUP_CONCAT(a.name ORDER BY a.name) AS albums
        FROM
            itunes.label l
        JOIN
            itunes.creator c ON l.id = c.label_id
        JOIN
            itunes.album a ON c.authorization_id = a.creator_authorization_id
        GROUP BY
            l.id, c.authorization_id
        ORDER BY
            l.id, c.authorization_id;
        """)

        # Виконання запиту та отримання результату
        result = db.session.execute(query).mappings().all()

        # Повертаємо список словників, де кожен рядок - це результат запиту
        return [dict(row) for row in result]
