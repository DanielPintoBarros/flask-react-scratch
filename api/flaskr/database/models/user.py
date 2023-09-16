from flaskr.database.db import psql
from flaskr.tools.enums import UserPermissionEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid


class UserModel(psql.Model):
    __tablename__ = "users"
    id = psql.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default="gen_random_uuid()",
    )
    permission = psql.Column(psql.Enum(UserPermissionEnum))
    first_name = psql.Column(psql.String(127))
    last_name = psql.Column(psql.String(127))
    email = psql.Column(psql.String(255))  # unique
    password = psql.Column(psql.String(255))

    @classmethod
    def find_by_id(cls, _id: str) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()
