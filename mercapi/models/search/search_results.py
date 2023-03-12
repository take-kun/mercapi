from copy import copy
from dataclasses import dataclass, field
from typing import List

from mercapi.models.base import ResponseModel
from mercapi.models.search import SearchResultItem, Meta
from mercapi.requests import SearchRequestData
from mercapi.util.errors import IncorrectRequestError


@dataclass
class SearchResults(ResponseModel):
    meta: Meta
    items: List[SearchResultItem]
    _request: SearchRequestData = field(init=False, compare=False, repr=False)

    async def next_page(self) -> "SearchResults":
        if self.meta.next_page_token == "":
            raise IncorrectRequestError(
                "Cannot fetch new page of search results, you are probably on the last page"
            )
        new_request = copy(self._request)
        new_request.page_token = self.meta.next_page_token
        return await self._mercapi._search_impl(new_request)

    async def prev_page(self) -> "SearchResults":
        if self.meta.prev_page_token == "":
            raise IncorrectRequestError(
                "Cannot fetch previous page of search results, you are probably on the first page"
            )
        new_request = copy(self._request)
        new_request.page_token = self.meta.prev_page_token
        return await self._mercapi._search_impl(new_request)
