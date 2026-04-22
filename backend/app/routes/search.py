from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.demo_content import search_users

search_bp = Blueprint("search", __name__, url_prefix="/api/search")


@search_bp.get("/users")
@jwt_required()
def users():
    return jsonify(
        search_users(
            query=request.args.get("q", ""),
            niveau=request.args.get("niveau", ""),
        )
    )
