from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from flaskr.database.models.user import UserModel
from flaskr.schemas.user import (
    LoginRequestSchema,
    LoginResponseSchema,
    TokenRefreshResponseSchema,
)
from passlib.hash import pbkdf2_sha256


blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(LoginRequestSchema)
    @blp.response(200, LoginResponseSchema)
    def post(self, login_data):
        user = UserModel.find_by_email(login_data["email"].lower())

        if user and pbkdf2_sha256.verify(login_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        abort(401, message="Invalid credentials.")


@blp.route("/refreshToken")
class UserTokenRefresh(MethodView):
    @blp.response(200, TokenRefreshResponseSchema)
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id, fresh=False)

        return {"access_token": new_token}, 200


"""
@blp.route("/register")
class UserRegister(MethodView):
    @jwt_required()
    def post(self):
        pass
"""
