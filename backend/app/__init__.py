from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_socketio import SocketIO

from config import get_config

# Extensions — initialisées sans app (pattern Application Factory)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    # Init des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    socketio.init_app(app, cors_allowed_origins="*", async_mode="eventlet")

    # Import modèles — nécessaire pour que Flask-Migrate les détecte
    from app.models import user, follow  # noqa: F401

    return app
