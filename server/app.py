import os
from decimal import getcontext
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from extensions import db, jwt
from views import register_blueprints
import config

load_dotenv()
getcontext().prec = 6


def create_app():
    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
        JWT_TOKEN_LOCATION=['cookies'],
        JWT_COOKIE_SECURE=False,
        JWT_COOKIE_SAMESITE='Lax',
        JWT_ACCESS_COOKIE_NAME='access_token',
        JWT_COOKIE_CSRF_PROTECT=False
    )

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=config.SERVER_HOST, port=config.SERVER_PORT, debug=config.DEBUG_MODE)
