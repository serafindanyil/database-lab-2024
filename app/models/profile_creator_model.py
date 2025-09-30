from app.extensions import db

class ProfileCreator(db.Model):
    __tablename__ = 'profile_creator'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    picture_link = db.Column(db.String(150))
    bio = db.Column(db.String(500))

    creators = db.relationship('Creator', back_populates='profile_creator')