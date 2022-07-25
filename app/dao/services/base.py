from typing import TypeVar, Generic, List

from app.dao.base import BaseDAO
from app.dao.services.exceptions import ItemNotFound

T = TypeVar('T', bound=BaseDAO)


class BaseService(Generic[T]):
    def __init__(self, dao: T, *args, **kwargs):
        self.dao = dao

    def get_one(self, item_id: int) -> object:
        item = self.dao.get_one(item_id)
        if not item:
            raise ItemNotFound
        return item

    def get_all(self, page: str) -> List[object]:
        items = self.dao.get_all(page, sort=False)

        if not items:
            raise ItemNotFound
        return items
