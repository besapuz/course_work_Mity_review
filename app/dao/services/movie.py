from typing import List
from app.dao.models.movie import Movie
from app.dao.services.base import BaseService
from app.dao.services.exceptions import ItemNotFound


class MovieService(BaseService):

    def get_all(self, page: str = None, status: str = None) -> List:

        check_status = status == 'new'
        if not check_status:
            movies = self.dao.get_all(page, sort=False)

        movies = self.dao.get_all(page, sort=True)
        if not movies:
            raise ItemNotFound

        return movies
