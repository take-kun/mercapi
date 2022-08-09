from typing import List

from mercapi.models import SearchResultItem
from mercapi.models.base import ResponseModel, Extractors


class Items(ResponseModel):
    _required_properties = [
        ('data', 'items', Extractors.get_list_of_model('data', SearchResultItem)),
    ]
    _optional_properties = []

    def __init__(self, items: List[SearchResultItem]):
        super().__init__()
        self.items = items
