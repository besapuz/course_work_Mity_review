from typing import List

from app.dao.director import DirectorDAO
from app.dao.genre import GenreDAO
from app.dao.movie import MovieDAO
from app.dao.user import UserDAO
from app.dao.services.exceptions import ItemNotFound


class BaseService:
    def __init__(self, dao: MovieDAO | GenreDAO | DirectorDAO | UserDAO):
        self.dao = dao

    def get_one(self, item_id: int) -> object:
        item = self.dao.get_one(item_id)
        if not item:
            raise ItemNotFound
        return item

    def get_all(self, page: str = None) -> List[object]:
        items = self.dao.get_all(page, sort=False)

        if not items:
            raise ItemNotFound
        return items
