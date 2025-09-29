from .authorization_routes import bp as authorization_bp
from .user_routes import bp as user_bp
from .review_routes import bp as review_bp
from .label_routes import bp as lable_bp


def init_app(app):
    app.register_blueprint(authorization_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(lable_bp)
