from flask import Flask, render_template
from flask_restx import Api

from config import Config
from app.create_db import db
from app.views.user import user_ns
from app.views.auth import auth_ns
from app.views.genres import genre_ns
from app.views.director import director_ns
from app.views.movies import movies_ns

api = Api(title="Flask Course Project 3", doc="/docs")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    api.init_app(app)

    api.add_namespace(director_ns)

    return app