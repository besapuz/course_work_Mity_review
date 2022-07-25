class Config:
    JSON_AS_ASCII = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///movies.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_JSON = {'ensure_ascii': False, 'indent': 4}
    HASH_NAME = 'sha256'
    PWD_HASH_SALT = b'secret here'
    PWD_HASH_ITERATIONS = 100_000
    JWT_SECRET = "random_secret"
    JWT_ALGORITHM = "HS256"
    TOKEN_EXPIRE_MINUTES = 15
    TOKEN_EXPIRE_DAYS = 130
    ITEMS_PER_PAGE = 12
