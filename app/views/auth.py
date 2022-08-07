from flask import request
from flask_restx import Namespace, Resource, abort
from app.container import auth_service, user_service
from app.dao.services.exceptions import ItemNotFound, WrongPassword, UserAlreadyExists, ValidationError, InvalidToken
from app.dao.models.user import UserSchema

auth_ns = Namespace('auth')
user_schema = UserSchema()


@auth_ns.route('/register/')
class AuthView(Resource):
    def post(self):

        credentials = {
            'email': request.json.get('email'),
            'password': request.json.get('password')
        }
        if None in credentials.values():
            abort(400, 'Wrong fields passed')

        try:
            data = user_schema.load(credentials)
            user = user_service.create(data)
            return "", 201, {"location": f"/user/{user.id}"}
        except ValidationError:
            abort(400, 'Not valid data passed')
        except UserAlreadyExists:
            abort(400, 'User already exists')


@auth_ns.route('/login/')
class LoginView(Resource):
    def post(self):

        credentials = {
            'email': request.json.get('email'),
            'password': request.json.get('password')
        }
        if None in credentials.values():
            abort(400, 'Not valid data passed')

        try:

            tokens = auth_service.generate_tokens(credentials)
            return tokens, 201
        except ItemNotFound:
            abort(404, 'User not found')
        except WrongPassword:
            abort(401, 'Incorrect password')

    def put(self):
        try:

            refresh_token = request.json.get('refresh_token')
            if not refresh_token:
                abort(400, 'Not valid data passed')

            tokens = auth_service.approve_token(refresh_token)
            return tokens, 201

        except InvalidToken:
            abort(401, 'Invalid token passed')
