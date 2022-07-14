from typing import List

from mercapi.models import ResponseModel
from mercapi.models.search import SearchResultItem
from mercapi.util.errors import ParseAPIResponseError


class SearchResults(ResponseModel):
    def __init__(self, items: List[SearchResultItem]):
        self.items = items

    def __repr__(self):
        return f'{__name__}.{self.__class__}'

    @classmethod
    def from_dict(cls, d: dict):
        items_raw = d.get('items')
        if items_raw is None or type(items_raw) != list:
            raise ParseAPIResponseError('Failed to retrieve list of items from search query response')
        items = [SearchResultItem.from_dict(i) for i in items_raw]
        return SearchResults(items)

    def as_dict(self) -> dict:
        return {'items': [i.as_dict() for i in self.items]}
