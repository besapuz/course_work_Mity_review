import base64
import hashlib
import hmac

from werkzeug.exceptions import MethodNotAllowed

from app.dao.models.user import User
from app.dao.services.base import BaseService
from app.dao.services.exceptions import UserNotFound
from app.dao.user import UserDAO
from flask import current_app


class UserService(BaseService):

    def get_by_email(self, email: str) -> User:
        user = self.dao.get_by_email(email)
        return user

    def get_hash(self, password: str) -> str:
        hashed = hashlib.pbkdf2_hmac(
            hash_name=current_app.config['HASH_NAME'],
            salt=current_app.config['PWD_HASH_SALT'],
            iterations=current_app.config['PWD_HASH_ITERATIONS'],
            password=password.encode('utf-8'))
        return base64.b64encode(hashed).decode('utf-8')

    def create(self, user):
        user['password'] = self.get_hash(user['password'])
        self.dao.create(user)

    def update_user_info(self, data: dict, email: str) -> None:
        if not self.get_by_email(email):
            raise UserNotFound
        if 'password' not in data.keys() and 'email' not in data.keys():
            self.dao.update_by_email(data, email)
        else:
            raise MethodNotAllowed

    def compare_passwords(self, password_hash: str, other_password: str) -> bool:
        hash_digest = base64.b64encode(hashlib.pbkdf2_hmac(
            hash_name=current_app.config['HASH_NAME'],
            password=other_password.encode('utf-8'),
            salt=current_app.config['PWD_HASH_SALT'],
            iterations=current_app.config['PWD_HASH_ITERATIONS']
        )).decode('utf-8')

        return hmac.compare_digest(password_hash, hash_digest)

    def update_passwords(self, email: str, password_old: str, password_new: str) -> None:
        user = self.get_by_email(email)
        data = {'password': self.get_hash(password_new)}
        self.dao.update_by_email(data, email)

    def update_password(self, data: dict, email: str) -> None:
        user = self.get_by_email(email)
        current_password = data.get('old_password')
        new_password = data.get('new_password')

        if None in [current_password, new_password]:
            raise MethodNotAllowed
        data = {
            'password': self.get_hash(current_password)

        }
        self.dao.update_by_email(data, email)
