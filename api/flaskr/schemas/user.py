from marshmallow import Schema, fields


class AuthRequestSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AuthResponseSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()


class TokenRefreshResponseSchema(Schema):
    access_token = fields.Str()
