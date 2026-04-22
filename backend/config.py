import os
import secrets
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SQLITE_PATH = BASE_DIR / "instance" / "tinamu.db"
DEFAULT_SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _normalize_sqlite_uri(database_url: str) -> str:
    if not database_url.startswith("sqlite:"):
        return database_url
    if database_url == "sqlite:///:memory:":
        return database_url

    relative_prefix = "sqlite:///"
    absolute_prefix = "sqlite:////"

    if database_url.startswith(absolute_prefix):
        sqlite_path = Path("/" + database_url.removeprefix(absolute_prefix))
    elif database_url.startswith(relative_prefix):
        sqlite_path = (BASE_DIR / database_url.removeprefix(relative_prefix)).resolve()
    else:
        return database_url

    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{sqlite_path}"


def _default_database_uri() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return _normalize_sqlite_uri(database_url)
    return _normalize_sqlite_uri(f"sqlite:///{DEFAULT_SQLITE_PATH}")


def _engine_options(database_uri: str) -> dict:
    if database_uri.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}}
    return {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    DEBUG = False
    TESTING = False

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = _default_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = _engine_options(SQLALCHEMY_DATABASE_URI)

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or secrets.token_hex(32)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"check_same_thread": False}}


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config_map.get(env, DevelopmentConfig)
