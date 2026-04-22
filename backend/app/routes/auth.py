from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from app import bcrypt, db
from app.models.user import NiveauEnum, User
from app.services.demo_content import ensure_seed_users, get_current_user, serialize_user

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def _error(message: str, status: int = 400):
    return jsonify({"message": message}), status


@auth_bp.post("/register")
def register():
    ensure_seed_users()
    payload = request.get_json(silent=True) or {}

    required_fields = ["student_id", "email_univ", "nom", "prenom", "password", "niveau"]
    missing = [field for field in required_fields if not str(payload.get(field, "")).strip()]
    if missing:
        return _error(f"Champs manquants: {', '.join(missing)}", 422)

    email = payload["email_univ"].strip().lower()
    student_id = payload["student_id"].strip()

    if User.query.filter(
        (User.email_univ == email) | (User.student_id == student_id)
    ).first():
        return _error("Un compte existe deja avec cet email ou ce numero etudiant.", 409)

    try:
        niveau = NiveauEnum(payload["niveau"])
    except ValueError:
        return _error("Niveau invalide.", 422)

    user = User(
        student_id=student_id,
        email_univ=email,
        nom=payload["nom"].strip(),
        prenom=payload["prenom"].strip(),
        password_hash=bcrypt.generate_password_hash(payload["password"]).decode("utf-8"),
        niveau=niveau,
        specialite=str(payload.get("specialite", "")).strip() or None,
        bio=str(payload.get("bio", "")).strip() or None,
    )
    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Compte cree avec succes.",
                "user": serialize_user(user, include_private=True),
            }
        ),
        201,
    )


@auth_bp.post("/login")
def login():
    ensure_seed_users()
    payload = request.get_json(silent=True) or {}
    identifier = str(payload.get("email_univ") or payload.get("identifier") or "").strip().lower()
    password = str(payload.get("password", ""))

    if not identifier or not password:
        return _error("Identifiant et mot de passe requis.", 422)

    user = User.query.filter(
        (User.email_univ == identifier) | (User.student_id == identifier)
    ).first()
    if user is None or not bcrypt.check_password_hash(user.password_hash, password):
        return _error("Identifiants invalides.", 401)

    return jsonify(
        {
            "access_token": create_access_token(identity=user.id),
            "refresh_token": create_refresh_token(identity=user.id),
            "user": serialize_user(user, include_private=True),
        }
    )


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user = get_current_user(get_jwt_identity())
    return jsonify({"access_token": create_access_token(identity=user.id)})


@auth_bp.get("/me")
@jwt_required()
def me():
    user = get_current_user(get_jwt_identity())
    return jsonify(serialize_user(user, include_private=True))


@auth_bp.put("/me")
@jwt_required()
def update_me():
    user = get_current_user(get_jwt_identity())
    payload = request.get_json(silent=True) or {}

    for field in ("bio", "avatar_url", "specialite"):
        if field in payload:
            value = str(payload[field]).strip()
            setattr(user, field, value or None)

    db.session.commit()
    return jsonify(
        {
            "message": "Profil mis a jour.",
            "user": serialize_user(user, include_private=True),
        }
    )


@auth_bp.post("/logout")
@jwt_required(optional=True)
def logout():
    return jsonify({"message": "Session locale terminee."})
