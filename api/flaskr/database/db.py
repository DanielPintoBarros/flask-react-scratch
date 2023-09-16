from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis


psql = SQLAlchemy()
redis_client = FlaskRedis()
