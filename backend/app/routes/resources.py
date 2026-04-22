from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.demo_content import create_resource, list_resources

resources_bp = Blueprint("resources", __name__, url_prefix="/api/resources")


def _error(message: str, status: int = 400):
    return jsonify({"message": message}), status


@resources_bp.get("")
@jwt_required()
def resources_list():
    return jsonify(list_resources(request.args.to_dict()))


@resources_bp.post("")
@jwt_required()
def resource_create():
    try:
        resource = create_resource(request.get_json(silent=True) or {})
    except ValueError as exc:
        return _error(str(exc), 422)
    return jsonify(resource), 201
