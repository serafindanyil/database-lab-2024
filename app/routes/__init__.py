from .genre_routes import bp as genre_bp

def init_app(app):
    app.register_blueprint(genre_bp)
