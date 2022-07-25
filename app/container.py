from app.create_db import db
from app.dao.models.director import Director
from app.dao.models.genre import Genre
from app.dao.models.movie import Movie
from app.dao.models.user import User
from app.dao.movie import MovieDAO
from app.dao.genre import GenreDAO
from app.dao.director import DirectorDAO
from app.dao.services.auth import AuthService
from app.dao.services.movie import MovieService
from app.dao.services.genre import GenreService
from app.dao.services.director import DirectorService
from app.dao.services.user import UserService
from app.dao.user import UserDAO

movie_dao = MovieDAO(session=db.session,model=Movie)
movie_service = MovieService(movie_dao)

genre_dao = GenreDAO(session=db.session,model=Genre)
genre_service = GenreService(genre_dao)

director_dao = DirectorDAO(session=db.session,model=Director)
director_service = DirectorService(director_dao)

user_dao = UserDAO(session=db.session,model=User)
user_service = UserService(user_dao)


auth_service = AuthService(dao=user_dao)
