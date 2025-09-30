from sqlalchemy import text

from app.extensions import db


class LabelDAO:
    def get_creator_for_every_label(self):
        bind = db.session.bind
        if bind and bind.dialect.name.startswith("mysql"):
            query = text(
                """
                SELECT 
                    l.name AS label_name,
                    GROUP_CONCAT(c.name ORDER BY c.name SEPARATOR ', ') AS creators
                FROM 
                    label l
                JOIN 
                    creator c ON l.id = c.label_id
                GROUP BY 
                    l.id
                ORDER BY 
                    l.name;
                """
            )
        else:
            query = text(
                """
                SELECT 
                    l.name AS label_name,
                    GROUP_CONCAT(c.name, ', ') AS creators
                FROM 
                    label l
                JOIN 
                    creator c ON l.id = c.label_id
                GROUP BY 
                    l.id
                ORDER BY 
                    l.name;
                """
            )

        result = db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

label_dao = LabelDAO()