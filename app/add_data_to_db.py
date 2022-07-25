from app.container import user_service
from app.dao.models.user import User


def add_data_to_db(app, db):

    """
    This function is used to add default users to database with passwords already encoded
    :param app:
    :param db:

    """

    with app.app_context():
        db.create_all()

        u1 = User(name="vasya", password="my_little_pony", role="user")
        u2 = User(name="oleg", password="qwerty", role="user")
        u3 = User(name="oleg", password="P@ssw0rd", role="admin")

        users = [u1, u2, u3]
        for user in users:
            password = user.password
            encoded_password = user_service.get_hash(password)
            user.password = encoded_password

        with db.session.begin():
            db.session.add_all(users)
