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
    # threading = compatible Python 3.13 (eventlet ne l'est pas)
    socketio.init_app(app, cors_allowed_origins="*", async_mode="threading")

    # Import modèles — nécessaire pour que Flask-Migrate les détecte
    from app.models import user, follow  # noqa: F401

    # JWT blacklist — vérifie chaque token entrant
    from app.services.auth_service import is_token_revoked

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(_jwt_header, jwt_payload):
        return is_token_revoked(jwt_payload)

    # JWT error handlers (401 / 422 / token révoqué)
    from app.routes.auth import register_jwt_error_handlers
    register_jwt_error_handlers(jwt)

    # Blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
