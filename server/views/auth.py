from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import traceback

from extensions import db
from models import UserDetails
from services.auth import register_user, authenticate_user
from utils.validators import (
    ValidationError, required_fields, validate_email,
    validate_password, validate_username, validate_name
)
import config

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        required_fields(data, ["full_name", "username", "password", "email"])

        validate_name(data["full_name"])
        validate_username(data["username"])
        validate_password(data["password"])
        validate_email(data["email"])

        user, error = register_user(
            data["full_name"], data["username"], data["password"], data["email"]
        )
        if error:
            return jsonify({"msg": error}), 409

        return jsonify({"msg": f"User {data['full_name']} registered successfully"}), 201

    except ValidationError as e:
        return jsonify({"msg": e.message}), e.status_code
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({"msg": "Registration failed", "details": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        required_fields(data, ["username", "password"])

        access_token = authenticate_user(data["username"], data["password"])
        if not access_token:
            return jsonify({"msg": "Invalid username or password"}), 401

        response = make_response(jsonify({"msg": "Login successful"}))
        response.set_cookie(
            "access_token", access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=config.JWT_EXPIRY_DAYS * 24 * 60 * 60,
            path='/'
        )
        return response, 200

    except ValidationError as e:
        return jsonify({"msg": e.message}), e.status_code
    except Exception as e:
        traceback.print_exc()
        return jsonify({"msg": "Login failed", "details": str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({"msg": "Logged out"}))
    response.set_cookie("access_token", "", max_age=0, httponly=True, secure=False, samesite='Lax', path='/')
    return response, 200


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        return jsonify({
            "id": current_user,
            "username": claims.get("username"),
            "full_name": claims.get("full_name"),
            "email": claims.get("email"),
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"msg": "Failed to fetch user info"}), 500
