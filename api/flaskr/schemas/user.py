from marshmallow import Schema, fields


class AuthRequestSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AuthResponseSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()


class LogoutRequestSchema(Schema):
    refresh_token = fields.Str(required=True)


class TokenRefreshResponseSchema(Schema):
    access_token = fields.Str()


class ChangePasswordRequestSchema(Schema):
    old_password = fields.Str(required=True)
    confirm_old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)
