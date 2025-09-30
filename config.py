import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Клас конфігурації для Flask застосунку."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "a-hard-to-guess-string"

    DATABASE_URL = os.environ.get("DATABASE_URL")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = os.environ.get("DB_HOST") or "localhost"
    DB_PORT = os.environ.get("DB_PORT") or "3306"
    DB_NAME = os.environ.get("DB_NAME")

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    elif DB_USER and DB_PASS and DB_NAME:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ECHO = False

    if SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {"check_same_thread": False},
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": int(os.environ.get("DB_POOL_RECYCLE", 280)),
            "pool_size": int(os.environ.get("DB_POOL_SIZE", 5)),
            "max_overflow": int(os.environ.get("DB_MAX_OVERFLOW", 10)),
        }
