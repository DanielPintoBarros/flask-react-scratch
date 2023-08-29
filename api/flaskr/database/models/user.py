from flaskr.database.db import db
from flaskr.tools.enums import UserPermissionEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = db.Column(db.Integer)
    permission = db.Column(db.Enum(UserPermissionEnum))
    active_status = db.Column(db.Boolean)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))  # unique
    email_verified_at = db.Column(db.Time)
    password = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255))

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()
