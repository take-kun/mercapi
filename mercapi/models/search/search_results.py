from typing import List

from mercapi.models.base import Extractors, ResponseModel, ResponseProperty
from mercapi.models.search import SearchResultItem, Meta


class SearchResults(ResponseModel):
    _required_properties = [
        ResponseProperty("meta", "meta", Extractors.get_as_model("meta", Meta)),
        ResponseProperty(
            "items",
            "items",
            Extractors.get_list_with("items", lambda i: SearchResultItem.from_dict(i)),
        ),
    ]
    _optional_properties = []

    def __init__(self, meta: Meta, items: List[SearchResultItem]):
        super().__init__()
        self.meta = meta
        self.items = items
        self._request = None
