from app.extensions import db


class Creator(db.Model):
    __tablename__ = 'creator'

    id = db.Column(db.Integer, primary_key=True)
    release_date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(45), nullable=False)

    # ЗМІНЕНО: Імена колонок та зовнішніх ключів
    authorization_id = db.Column(db.Integer, db.ForeignKey('authorization.id'), nullable=False)
    label_id = db.Column(db.Integer, db.ForeignKey('label.id'), nullable=False)
    profile_creator_id = db.Column(db.Integer, db.ForeignKey('profile_creator.id'), nullable=False)

    authorization = db.relationship('Authorization', back_populates='creators')
    label = db.relationship('Label', back_populates='creators')
    profile_creator = db.relationship('ProfileCreator', back_populates='creators')
    albums = db.relationship('Album', back_populates='creator', cascade="all, delete-orphan")
    song_creators = db.relationship('SongHasCreator', back_populates='creator', cascade="all, delete-orphan")