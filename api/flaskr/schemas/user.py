from marshmallow import Schema, fields


class LoginRequestSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class LoginResponseSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()


class TokenRefreshResponseSchema(Schema):
    access_token = fields.Str()
