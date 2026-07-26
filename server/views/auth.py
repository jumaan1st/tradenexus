from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import traceback

from extensions import db
from models import UserDetails
from services.auth import register_user, authenticate_user
import config

auth_bp = Blueprint('auth', __name__)


def _handle_error(e, message="Something went wrong"):
    traceback.print_exc()
    return {"error": message, "details": str(e)}


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ["full_name", "username", "password", "email"]

    if not all(data.get(field) for field in required_fields):
        return jsonify({"msg": "All fields are required"}), 400

    user, error = register_user(
        data["full_name"], data["username"], data["password"], data["email"]
    )
    if error:
        return jsonify({"msg": error}), 409

    return jsonify({"msg": f"User {data['full_name']} registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    access_token = authenticate_user(username, password)
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


@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({"msg": "Logged out"}))
    response.set_cookie("access_token", "", max_age=0, httponly=True, secure=False, samesite='Lax', path='/')
    return response, 200


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    claims = get_jwt()
    return jsonify({
        "id": current_user,
        "username": claims.get("username"),
        "full_name": claims.get("full_name"),
        "email": claims.get("email"),
    }), 200
