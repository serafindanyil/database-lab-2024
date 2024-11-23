from .authorization_routes import bp as authorization_bp
from .user_routes import bp as user_bp


def init_app(app):
    app.register_blueprint(authorization_bp)
    app.register_blueprint(user_bp)
