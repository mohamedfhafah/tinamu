from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.demo_content import (
    get_current_user,
    get_leaderboard,
    get_quiz,
    list_quizzes,
    submit_quiz,
)

quiz_bp = Blueprint("quiz", __name__, url_prefix="/api/quiz")


def _error(message: str, status: int = 400):
    return jsonify({"message": message}), status


@quiz_bp.get("")
@jwt_required()
def list_all_quizzes():
    return jsonify(list_quizzes())


@quiz_bp.get("/leaderboard")
@jwt_required()
def leaderboard():
    return jsonify(get_leaderboard())


@quiz_bp.get("/<quiz_id>")
@jwt_required()
def quiz_detail(quiz_id: str):
    try:
        return jsonify(get_quiz(quiz_id))
    except ValueError as exc:
        return _error(str(exc), 404)


@quiz_bp.post("/<quiz_id>/start")
@jwt_required()
def quiz_start(quiz_id: str):
    try:
        return jsonify(get_quiz(quiz_id))
    except ValueError as exc:
        return _error(str(exc), 404)


@quiz_bp.post("/<quiz_id>/submit")
@jwt_required()
def quiz_submit(quiz_id: str):
    current_user = get_current_user(get_jwt_identity())
    payload = request.get_json(silent=True) or {}
    try:
        return jsonify(submit_quiz(current_user, quiz_id, payload.get("answers", {})))
    except ValueError as exc:
        return _error(str(exc), 404)
