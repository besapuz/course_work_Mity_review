from marshmallow import fields, Schema
from app.create_db import db
from app.dao.models.base import BaseModel


class Director(BaseModel, db.Model):
    __tablename__ = 'director'
    name = db.Column(db.String(100), unique=True, nullable=False)


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
