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
