from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from datetime import timedelta
from flaskr.database.db import psql, redis_client
from flaskr.resources.user import blp as UserBlueprint

from flask_redis import FlaskRedis
from mockredis import MockRedis

# from flaskr.resources.item import blp as ItemBlueprint
# from flaskr.resources.store import blp as StoreBlueprint
# from flaskr.resources.tag import blp as TagBlueprint

import os


load_dotenv()


def create_app(psql_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-docs"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = psql_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["REDIS_URL"] = os.getenv("REDIS_URL", "redis://")
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-env")
    ACCESS_TOKEN_EXPIRATION_TIME = int(
        os.getenv("ACCESS_TOKEN_EXPIRES", "3600")
    )  # 3600 seconds == 1 hour
    REFRESH_TOKEN_EXPIRATION_TIME = int(
        os.getenv("REFRESH_TOKEN_EXPIRES", "2592000")
    )  # 2592000 seconds == 30 days
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        seconds=ACCESS_TOKEN_EXPIRATION_TIME
    )
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
        seconds=REFRESH_TOKEN_EXPIRATION_TIME
    )

    psql.init_app(app)
    migrate = Migrate(app, psql)
    redis_client.init_app(app)

    jwt = JWTManager(app)

    api = Api(app)

    @app.route("/")
    def index():
        return """
    Pipesun Backend version: {}.
    Try '/swagger-docs' endpoint for API's documentation
    """.format(
            app.config["API_VERSION"]
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        token = jwt_payload["jti"]
        is_blocked = bool(redis_client.get(token))
        return is_blocked

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    api.register_blueprint(UserBlueprint)

    return app
