from marshmallow import Schema, fields
from app.create_db import db
from app.dao.models.base import BaseModel
from app.dao.models.genre import Genre


class User(BaseModel):
    __tablename__ = 'users'
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255))
    favourite_genre = db.Column(db.ForeignKey(Genre.id))


class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()
    surname = fields.String()
    email = fields.String()
    password_hash = fields.String()
    role = fields.String()
