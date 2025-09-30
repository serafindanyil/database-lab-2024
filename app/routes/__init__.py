from flask_restx import Api

from .authorization_routes import authorization_ns
from .label_routes import label_ns
from .review_routes import review_ns
from .user_routes import user_ns


api = Api(
    title="Music Library API",
    version="1.0",
    description="Interactive documentation for the music platform",
    doc="/docs",
)

api.add_namespace(authorization_ns)
api.add_namespace(user_ns)
api.add_namespace(review_ns)
api.add_namespace(label_ns)


def init_app(app):
    api.init_app(app)
