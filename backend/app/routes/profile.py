from __future__ import annotations

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.demo_content import (
    follow_user,
    get_current_user,
    get_profile,
    get_profile_stats,
    unfollow_user,
)

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")


def _error(message: str, status: int = 400):
    return jsonify({"message": message}), status


@profile_bp.get("/<user_id>")
@jwt_required()
def profile(user_id: str):
    current_user = get_current_user(get_jwt_identity())
    try:
        return jsonify(get_profile(user_id, current_user))
    except ValueError as exc:
        return _error(str(exc), 404)


@profile_bp.get("/<user_id>/stats")
@jwt_required()
def profile_stats(user_id: str):
    try:
        return jsonify(get_profile_stats(user_id))
    except ValueError as exc:
        return _error(str(exc), 404)


@profile_bp.post("/<user_id>/follow")
@jwt_required()
def follow(user_id: str):
    current_user = get_current_user(get_jwt_identity())
    try:
        return jsonify(follow_user(current_user, user_id))
    except ValueError as exc:
        return _error(str(exc), 422)


@profile_bp.delete("/<user_id>/follow")
@jwt_required()
def unfollow(user_id: str):
    current_user = get_current_user(get_jwt_identity())
    try:
        return jsonify(unfollow_user(current_user, user_id))
    except ValueError as exc:
        return _error(str(exc), 422)
