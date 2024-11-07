from .genre_routes import bp as genre_bp
from .song_routes import bp as song_bp
from .authorization_routes import bp as authorization_bp
from .label_routes import bp as label_bp
from .profile_creator_routes import bp as profile_creator_bp
from .creator_routes import bp as creator_bp
from .album_routes import bp as album_bp
from .profile_user_routes import bp as profile_user_bp
from .subcription_routes import bp as subcription_bp
from .user_routes import bp as user_bp
from .download_routes import bp as download_bp
from .song_has_creator_routes import bp as song_has_creator_bp
from .song_has_album_routes import bp as song_has_album_bp

def init_app(app):
    app.register_blueprint(genre_bp)
    app.register_blueprint(song_bp)
    app.register_blueprint(authorization_bp)
    app.register_blueprint(label_bp)
    app.register_blueprint(profile_creator_bp)
    app.register_blueprint(creator_bp)
    app.register_blueprint(album_bp)
    app.register_blueprint(profile_user_bp)
    app.register_blueprint(subcription_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(download_bp)
    app.register_blueprint(song_has_creator_bp)
    app.register_blueprint(song_has_album_bp)
