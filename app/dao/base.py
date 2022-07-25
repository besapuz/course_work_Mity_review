from typing import List

from flask import current_app
from sqlalchemy import desc
from sqlalchemy.orm import Session


class BaseDAO:
    def __init__(self, session: Session, model):
        self.session = session
        self.model = model

    def get_one(self, item_id: int) -> object:
        item = self.session.query(self.model).get(item_id)
        return item

    def get_all(self, page: str = None, sort: bool = False) -> List[object]:
        items = self.session.query(self.model).all()
        if sort:
            items = items.order_by(desc(self.model.year))
        if page:
            items = items.limit(current_app.config['ITEMS_PER_PAGE']).offset(
                page * current_app.config['ITEMS_PER_PAGE'] - current_app.config['ITEMS_PER_PAGE'])

        return items.all()

