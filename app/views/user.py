from flask import request, abort
from flask_restx import Namespace, Resource
from app.container import user_service, auth_service
from app.dao.models.user import UserSchema
from app.dao.services.exceptions import UserNotFound, WrongPassword


user_ns = Namespace('users')

users_schema = UserSchema(many=True)
user_schema = UserSchema()


@user_ns.route('/')
class UserView(Resource):
    @auth_service.auth_required
    def get(self):
        try:
            auth_data = request.headers['Authorization']
            token = auth_data.split("Bearer ")[-1]
            email = auth_service.get_email_from_jwt(token)

            user = user_service.get_by_email(email)
            return users_schema.dump(user), 200

        except UserNotFound:
            abort(404, 'User not found')

    @auth_service.auth_required
    def patch(self):
        try:
            auth_data = request.headers['Authorization']
            token = auth_data.split("Bearer ")[-1]
            email = auth_service.get_email_from_jwt(token)
            updated_data = user_schema.dump(request.get_json())
            user_service.update_user_info(updated_data, email)
            return "", 200

        except UserNotFound:
            abort(404, 'User not found')


@user_ns.route('/password/')
class PasswordView(Resource):
    @auth_service.auth_required
    def put(self):
        try:
            auth_data = request.headers['Authorization']
            token = auth_data.split("Bearer ")[-1]
            email = auth_service.get_email_from_token(token)
            passwords = request.get_json()
            user_service.update_password(passwords, email)
            return "", 200
        except UserNotFound:
            abort(404, 'User not found')
        except WrongPassword:
            abort(401, 'Incorrect password')
