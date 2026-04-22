from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.demo_content import (
    create_conversation,
    get_conversation,
    get_current_user,
    list_conversations,
    send_message,
)

conversations_bp = Blueprint("messages", __name__, url_prefix="/api/conversations")


def _error(message: str, status: int = 400):
    return jsonify({"message": message}), status


@conversations_bp.get("")
@jwt_required()
def all_conversations():
    current_user = get_current_user(get_jwt_identity())
    return jsonify(list_conversations(current_user))


@conversations_bp.post("")
@jwt_required()
def create_thread():
    current_user = get_current_user(get_jwt_identity())
    payload = request.get_json(silent=True) or {}
    target_user_id = str(payload.get("user_id", "")).strip()
    if not target_user_id:
        return _error("user_id requis.", 422)
    try:
        conversation = create_conversation(current_user, target_user_id)
        return jsonify(get_conversation(conversation["id"], current_user)), 201
    except ValueError as exc:
        return _error(str(exc), 422)


@conversations_bp.get("/<conversation_id>/messages")
@jwt_required()
def messages(conversation_id: str):
    current_user = get_current_user(get_jwt_identity())
    try:
        return jsonify(get_conversation(conversation_id, current_user))
    except ValueError as exc:
        return _error(str(exc), 404)


@conversations_bp.post("/<conversation_id>/messages")
@jwt_required()
def add_message(conversation_id: str):
    current_user = get_current_user(get_jwt_identity())
    payload = request.get_json(silent=True) or {}
    try:
        message = send_message(current_user, conversation_id, str(payload.get("body", "")))
    except ValueError as exc:
        return _error(str(exc), 422)
    return jsonify(message), 201
