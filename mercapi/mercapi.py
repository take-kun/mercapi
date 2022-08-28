import random
import uuid
from typing import Optional, List

import httpx
from ecdsa import SigningKey, NIST256p
from httpx import Request

from mercapi.models import SearchResults, Item, Profile, Items
from mercapi.models.base import ResponseModel
from mercapi.requests import SearchRequestData
from mercapi.util import jwt


class Mercapi:
    """Main class of the module containing all implemented
    wrappers of Mercari API.

    A random key-pair will be generated during the class instantiation.
    It is used for signing all HTTP requests sent in the course of methods execution.

    **Avoid instantiating this class more than once in a single runtime.**
    """

    _user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
    )
    _headers = {
        "User-Agent": _user_agent,
        "X-Platform": "web",
    }

    def __init__(self):
        self._uuid = str(uuid.UUID(int=random.getrandbits(128)))
        self._key = SigningKey.generate(NIST256p)
        self._client = httpx.AsyncClient()
        ResponseModel.set_mercapi(self)

    def _sign_request(self, request: Request) -> Request:
        request.headers["DPoP"] = jwt.generate_dpop(
            str(request.url),
            request.method,
            self._key,
            {
                "uuid": self._uuid,
            },
        )
        return request

    async def search(
        self,
        query: str,
        categories: List[int] = [],
        brands: List[int] = [],
        sizes: List[int] = [],
        price_min: int = None,
        price_max: int = None,
        item_conditions: List[int] = [],
        shipping_payer: List[int] = [],
        colors: List[int] = [],
        shipping_methods: List[SearchRequestData.ShippingMethod] = [],
        status: List[SearchRequestData.Status] = [],
    ) -> SearchResults:
        """Perform basic search and return list of items and metadata.
        This method reflects the action of using search bar at the top of the website.

        All parameters except for `query` must be provided as lists of ints
        referencing facets IDs supplied by Mercari API. Refer to files in
        `docs/facets` directory enumerating available facets and their identifiers.

        These files can be updated at any time by running `utils/fetch_facets.py`.

        :param query: string results should match (e.g. what you type in top search bar)
        :param categories: filter results by categories (カテゴリー)
        :param brands: filter results by brands (ブランド)
        :param sizes: filter results by sizes (サイズ)
        :param price_min: set results minimum price (価格, first textbox)
        :param price_max: set results maximum price (価格, second textbox)
        :param item_conditions: filter results by conditions  (商品の状態)
        :param shipping_payer: filter results by party responsible for reimbursing shipping costs (配送料の負担)
        :param colors: filter results by colors (色)
        :param shipping_methods: filter results by available shipping methods (発送オプション)
        :param status: filter results by listing statuses (販売状況)
        :return: List of search results (items) and metadata (e.g. total count)
        """
        request = SearchRequestData(
            SearchRequestData.SearchConditions(
                query,
                categories,
                brands,
                sizes,
                price_min,
                price_max,
                item_conditions,
                shipping_payer,
                colors,
                shipping_methods,
                status,
            ),
        )
        res = await self._client.send(self._search(request))
        body = res.json()
        return SearchResults.from_dict(body)

    def _search(self, search_request_data: SearchRequestData) -> Request:
        req = Request(
            "POST",
            "https://api.mercari.jp/v2/entities:search",
            json=search_request_data.data,
            headers=self._headers,
        )
        return self._sign_request(req)

    async def item(self, id_: str) -> Optional[Item]:
        """Fetch details of a single listing (item).
        This method reflects the action of loading single item view.

        :param id_: id of a listing (item)
        :return: all available listing (item) properties
        """
        res = await self._client.send(self._item(id_))
        if res.status_code == 404:
            return None

        body = res.json()
        return Item.from_dict(body["data"])

    def _item(self, id_: str) -> Request:
        req = Request(
            "GET",
            "https://api.mercari.jp/items/get",
            params={"id": id_},
            headers=self._headers,
        )
        return self._sign_request(req)

    async def profile(self, id_: str) -> Optional[Profile]:
        """Fetch details of a single seller.
        This method reflects the action of loading single seller profile view.

        :param id_: id of a seller (profile)
        :return: all available seller (profile) properties
        """
        res = await self._client.send(self._profile(id_))
        if res.status_code == 404:
            return None

        body = res.json()
        return Profile.from_dict(body["data"])

    def _profile(self, id_: str) -> Request:
        req = Request(
            "GET",
            "https://api.mercari.jp/users/get_profile",
            params={"user_id": id_, "_user_format": "profile"},
            headers=self._headers,
        )
        return self._sign_request(req)

    async def items(self, profile_id: str) -> Optional[Items]:
        """Fetch all items sold by specified seller.
        This method reflects the action of loading single seller profile view.

        :param profile_id: ID of a seller
        :return: list of items sold by specified seller
        """
        res = await self._client.send(self._items(profile_id))
        if res.status_code == 404:
            return None

        body = res.json()
        return Items.from_dict(body)

    def _items(self, profile_id: str) -> Request:
        req = Request(
            "GET",
            "https://api.mercari.jp/items/get_items",
            params={
                "seller_id": profile_id,
                "limit": 30,
                "status": "on_sale,trading,sold_out",
            },
            headers=self._headers,
        )
        return self._sign_request(req)
