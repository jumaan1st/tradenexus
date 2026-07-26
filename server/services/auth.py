from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from extensions import db
from models import UserDetails
import config


def register_user(full_name, username, password, email):
    if UserDetails.query.filter_by(username=username).first():
        return None, "Username already exists"

    hashed_password = generate_password_hash(password)
    new_user = UserDetails(
        full_name=full_name,
        username=username,
        password=hashed_password,
        email=email
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user, None


def authenticate_user(username, password):
    user = UserDetails.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return None

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "full_name": user.full_name,
            "email": user.email,
            "username": user.username
        },
        expires_delta=timedelta(days=config.JWT_EXPIRY_DAYS)
    )
    return access_token
