from typing import List

from mercapi.models import ResponseModel
from mercapi.models.base import Extractors
from mercapi.models.search import SearchResultItem


class SearchResults(ResponseModel):
    _required_properties = [
        ('items', 'items', Extractors.get_list_with('items', lambda i: SearchResultItem.from_dict(i)))
    ]
    _optional_properties = []

    def __init__(self, items: List[SearchResultItem]):
        super().__init__()
        self.items = items
