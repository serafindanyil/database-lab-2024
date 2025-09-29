from app import db
from sqlalchemy import text


class label_dao:
    @staticmethod
    def get_creator_for_every_label():
        query = text("""
          SELECT 
    l.name AS label_name,
    GROUP_CONCAT(
        CONCAT(c.name, ': ', a.name) ORDER BY c.name, a.name
        SEPARATOR ', '
    ) AS creators_and_albums
FROM 
    itunes.label l
JOIN 
    itunes.creator c ON l.id = c.label_id
JOIN 
    itunes.album a ON c.authorization_id = a.creator_authorization_id
GROUP BY 
    l.id
ORDER BY 
    l.id;

           """)
        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]
