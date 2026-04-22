from app.routes.auth import auth_bp
from app.routes.feed import feed_bp
from app.routes.messages import conversations_bp
from app.routes.profile import profile_bp
from app.routes.quiz import quiz_bp
from app.routes.resources import resources_bp
from app.routes.search import search_bp


def register_blueprints(app):
    """Register every public API blueprint for the TinAMU demo backend."""
    for blueprint in (
        auth_bp,
        feed_bp,
        quiz_bp,
        resources_bp,
        conversations_bp,
        search_bp,
        profile_bp,
    ):
        app.register_blueprint(blueprint)
