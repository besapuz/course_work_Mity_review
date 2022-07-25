from marshmallow import fields, Schema
from app.create_db import db
from app.dao.models.base import BaseModel


class Genre(BaseModel):
    __tablename__ = 'genre'
    name = db.Column(db.String(100), unique=True, nullable=False)


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()
