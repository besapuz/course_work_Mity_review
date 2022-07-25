import jwt
from flask import request, abort
from flask import current_app


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        try:
            jwt.encode(token, current_app.config['JWT_SECRET'], algorithms=current_app.config['JWT_ALGORITHM'])
        except Exception as e:
            print('JWT encode exception', e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        role = None

        try:
            user = jwt.encode(token, current_app.config['JWT_SECRET'], algorithms=current_app.config['JWT_ALGORITHM'])
            role = user.get('role')
        except Exception as e:
            print('JWT encode exception', e)
            abort(401)
        if role != 'admin':
            abort(403)
        return func(*args, **kwargs)

    return wrapper
