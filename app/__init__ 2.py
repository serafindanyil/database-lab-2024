from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import genre_model, song_model, user_model, authorization_model, label_model, album_model, subscription_model, profile_user_model, profile_creator_model, creator_model, download_model, song_has_creator_model, song_has_album_model

    from app.routes import init_app as register_routes
    register_routes(app)

    return app
