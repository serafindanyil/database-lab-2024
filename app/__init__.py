from flask import Flask
from config import Config

from app.extensions import db, migrate
from app.routes import init_app as register_blueprints


def create_app(config_object: type[Config] | None = None) -> Flask:
	app = Flask(__name__)
	if config_object is not None:
		app.config.from_object(config_object)
	else:
		app.config.from_object(Config)

	app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
	app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

	db.init_app(app)
	migrate.init_app(app, db)

	with app.app_context():
		from app import models  # noqa: F401
		db.create_all()

	register_blueprints(app)

	@app.get("/health")
	def health_check() -> dict[str, str]:
		return {"status": "ok"}

	@app.cli.command("seed")
	def seed_command() -> None:
		from app.seeds import seed_database

		seed_database()

	return app
