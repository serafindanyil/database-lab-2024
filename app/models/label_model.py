from app.extensions import db

class Label(db.Model):
    __tablename__ = 'label'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False, unique=True)

    creators = db.relationship('Creator', back_populates='label')