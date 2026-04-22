from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.demo_content import (
    create_post,
    delete_post,
    get_current_user,
    list_feed,
    swipe_candidate,
)

feed_bp = Blueprint("feed", __name__, url_prefix="/api/feed")


def _error(message: str, status: int = 400):
    return jsonify({"message": message}), status


@feed_bp.get("")
@jwt_required()
def get_feed():
    current_user = get_current_user(get_jwt_identity())
    return jsonify(list_feed(current_user))


@feed_bp.post("/swipe")
@jwt_required()
def swipe():
    current_user = get_current_user(get_jwt_identity())
    payload = request.get_json(silent=True) or {}
    target_user_id = str(payload.get("user_id", "")).strip()
    direction = str(payload.get("direction", "")).strip()

    if not target_user_id or not direction:
        return _error("user_id et direction sont requis.", 422)

    try:
        result = swipe_candidate(current_user, target_user_id, direction)
    except ValueError as exc:
        return _error(str(exc), 422)
    return jsonify(result)


@feed_bp.get("/matches")
@jwt_required()
def matches():
    current_user = get_current_user(get_jwt_identity())
    return jsonify(list_feed(current_user)["matches"])


@feed_bp.post("/posts")
@jwt_required()
def add_post():
    current_user = get_current_user(get_jwt_identity())
    try:
        post = create_post(current_user, request.get_json(silent=True) or {})
    except ValueError as exc:
        return _error(str(exc), 422)
    return jsonify(post), 201


@feed_bp.delete("/posts/<post_id>")
@jwt_required()
def remove_post(post_id: str):
    current_user = get_current_user(get_jwt_identity())
    if not delete_post(current_user, post_id):
        return _error("Post introuvable ou non autorise.", 404)
    return jsonify({"message": "Post supprime."})
