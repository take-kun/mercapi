from dataclasses import dataclass
from typing import List

from mercapi.models.base import ResponseModel
from mercapi.models.search import SearchResultItem, Meta


@dataclass
class SearchResults(ResponseModel):
    meta: Meta
    items: List[SearchResultItem]
