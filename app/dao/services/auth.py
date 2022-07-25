import base64
import hashlib
import hmac
from typing import Optional, Dict
import datetime
import jwt
from app.dao.serialization.auth import AuthUserSchema
from flask import current_app
from app.dao.services.exceptions import UserNotFound, WrongPassword
from app.dao.user import UserDAO


class AuthService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_hash(self, password: str) -> str:
        hashed = hashlib.pbkdf2_hmac(
            hash_name=current_app.config['HASH_NAME'],
            salt=current_app.config['PWD_HASH_SALT'],
            iterations=current_app.config['PWD_HASH_ITERATIONS'],
            password=password.encode('utf-8')
        )
        return base64.b64encode(hashed).decode('utf-8')

    def compare_passwords(self, password_1: str, password_2: str) -> bool:
        return hmac.compare_digest(password_1, password_2)

    def generate_tokens(self, user: AuthUserSchema):

        payload = {
            'email': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
        }

        access_token = jwt.encode(payload, current_app.config['JWT_SECRET'],
                                  current_app.config['JWT_ALGORITHM'])

        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])

        refresh_token = jwt.encode(payload, current_app.config['JWT_SECRET'],
                                   current_app.config['JWT_ALGORITHM'])

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def register(self, email: str, password: str) -> AuthUserSchema:
        password_hash = self.get_hash(password)
        data = {
            'email': email,
            'password_hash': password_hash

        }
        return self.dao.create(data)

    def login(self, email: str, password: str) -> Dict[str, str]:

        user: Optional[AuthUserSchema] = self.dao.get_by_email(email=email)

        if user is None:
            raise UserNotFound
        print(user)
        password_hash = self.get_hash(password)

        if not self.compare_passwords(user['password_hash'], password_hash):
            raise WrongPassword

        return self.generate_tokens(user)
