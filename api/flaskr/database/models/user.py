from flaskr.database.db import db
from flaskr.tools.enums import UserPermissionEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default="gen_random_uuid()",
    )
    permission = db.Column(db.Enum(UserPermissionEnum))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))  # unique
    password = db.Column(db.String(255))

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @property
    def full_name(self) -> str:
        return " ".join([self.first_name, self.last_name])
