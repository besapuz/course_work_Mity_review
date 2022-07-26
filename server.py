from flask import Flask, render_template
from flask_cors import CORS
from flask_restx import Api

from app.create_db import db
from app.views.auth import auth_ns
from app.views.director import director_ns
from app.views.genres import genre_ns
from app.views.movies import movies_ns
from app.views.user import user_ns

cors = CORS()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    @app.route('/')
    def index():
        return render_template('index.html')

    cors.init_app(app)
    api = Api(app)
    db.init_app(app)

    api.add_namespace(genre_ns)
    api.add_namespace(director_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    return app
