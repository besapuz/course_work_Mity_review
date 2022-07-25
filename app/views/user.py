from flask import request
from flask_restx import Namespace, Resource
from app.container import user_service
from app.dao.models.user import UserSchema
from app.decorators import auth_required, admin_required

user_ns = Namespace('users')

users_schema = UserSchema(many=True)
user_schema = UserSchema()


@user_ns.route('/')
class UserView(Resource):
    def get(self):
        all_users = user_service.get_all()
        return users_schema.dump(all_users), 200


@user_ns.route('/<int:uid>')
class UserView(Resource):

    def get_by_username(self, username):
        user = user_service.get_by_username(username)
        return user_schema.dumps(user), 200

    def put(self, uid):
        data = request.get_json()
        data['uid'] = uid
        user_service.update(data)
        return '', 204
