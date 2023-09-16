from dotenv import load_dotenv
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
    decode_token,
)
from flask_smorest import Blueprint, abort
from flaskr.database.db import redis_client
from flaskr.database.models.user import UserModel
from flaskr.schemas.user import (
    AuthRequestSchema,
    AuthResponseSchema,
    LogoutRequestSchema,
    TokenRefreshResponseSchema,
)
from passlib.hash import pbkdf2_sha256


import os

blp = Blueprint("Users", "users", description="Operations on users")

load_dotenv()
ACCESS_TOKEN_EXPIRATION_TIME = int(
    os.getenv("ACCESS_TOKEN_EXPIRES", "3600")
)  # 3600 seconds == 1 hour
REFRESH_TOKEN_EXPIRATION_TIME = int(
    os.getenv("REFRESH_TOKEN_EXPIRES", "2592000")
)  # 2592000 seconds == 30 days


@blp.route("/auth")
class UserAuth(MethodView):
    @blp.arguments(AuthRequestSchema)
    @blp.response(200, AuthResponseSchema)
    def post(self, auth_data):
        user = UserModel.find_by_email(auth_data["email"].lower())

        if user and pbkdf2_sha256.verify(auth_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        abort(401, message="invalid credentials")


@blp.route("/refreshToken")
class UserTokenRefresh(MethodView):
    @blp.response(200, TokenRefreshResponseSchema)
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id, fresh=False)

        return {"access_token": new_token}, 200


@blp.route("/logout")
class UserLogout(MethodView):
    @blp.arguments(LogoutRequestSchema)
    @blp.response(200)
    @jwt_required()
    def post(self, logout_data):
        try:
            access_token = get_jwt()["jti"]

            refresh_token = decode_token(logout_data["refresh_token"].split(" ")[-1])[
                "jti"
            ]

            redis_client.set(access_token, 0)
            redis_client.expire(access_token, ACCESS_TOKEN_EXPIRATION_TIME)
            redis_client.set(refresh_token, 0)
            redis_client.expire(refresh_token, REFRESH_TOKEN_EXPIRATION_TIME)
        except:
            abort(400, message="refresh token not valid")
        return None, 200
