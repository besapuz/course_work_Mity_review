from flask import request
from flask_restx import Namespace, Resource, abort
from app.container import auth_service
from app.dao.serialization.auth import AuthRegisterRequest
from app.dao.services.exceptions import ItemNotFound, WrongPassword

auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class AuthView(Resource):
    def post(self):
        data = request.json
        validated_data = AuthRegisterRequest().load(data)

        auth_service.register(
            email=validated_data['email'],
            password=validated_data['password']

        )
        return "", 200


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
