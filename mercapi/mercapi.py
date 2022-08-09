import random
import uuid
from typing import Optional, List

import httpx
from ecdsa import SigningKey, NIST256p
from httpx import Request

from mercapi.models import SearchResults, Item, Profile
from mercapi.models.base import ResponseModel
from mercapi.requests import SearchRequestData
from mercapi.util import jwt


class Mercapi:
    _user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'
    _headers = {
        'User-Agent': _user_agent,
        'X-Platform': 'web',
    }

    def __init__(self):
        self._uuid = str(uuid.UUID(int=random.getrandbits(128)))
        self._key = SigningKey.generate(NIST256p)
        self._client = httpx.AsyncClient()
        ResponseModel.set_mercapi(self)

    def _sign_request(self, request: Request) -> Request:
        request.headers['DPoP'] = jwt.generate_dpop(
            str(request.url),
            request.method,
            self._key,
            {
                'uuid': self._uuid,
            }
        )
        return request

    async def search(self, query: str, categories: List[int] = [], brands: List[int] = [], sizes: List[int] = [],
                     price_min: int = None, price_max: int = None, item_conditions: List[int] = [],
                     shipping_payer: List[int] = [], colors: List[int] = [],
                     shipping_methods: List[SearchRequestData.ShippingMethod] = [],
                     status: List[SearchRequestData.Status] = []) -> SearchResults:
        res = await self._client.send(self._search(
            query, categories, brands, sizes, price_min, price_max, item_conditions, shipping_payer, colors,
            shipping_methods, status
        ))
        body = res.json()
        return SearchResults.from_dict(body)

    def _search(self, query: str, categories: List[int] = [], brands: List[int] = [], sizes: List[int] = [],
                price_min: int = None, price_max: int = None, item_conditions: List[int] = [],
                shipping_payer: List[int] = [], colors: List[int] = [],
                shipping_methods: List[SearchRequestData.ShippingMethod] = [],
                status: List[SearchRequestData.Status] = []) -> Request:
        data = SearchRequestData(
            query, categories, brands, sizes, price_min, price_max, item_conditions, shipping_payer,
            colors, shipping_methods, status,
        )
        req = Request('POST', 'https://api.mercari.jp/v2/entities:search',
                      json=data.data,
                      headers=self._headers
                      )
        return self._sign_request(req)

    async def item(self, id_: str) -> Optional[Item]:
        res = await self._client.send(self._item(id_))
        if res.status_code == 404:
            return None

        body = res.json()
        return Item.from_dict(body['data'])

    def _item(self, id_: str) -> Request:
        req = Request('GET', 'https://api.mercari.jp/items/get', params={'id': id_}, headers=self._headers)
        return self._sign_request(req)

    async def profile(self, id_: str) -> Optional[Profile]:
        res = await self._client.send(self._profile(id_))
        if res.status_code == 404:
            return None

        body = res.json()
        return Profile.from_dict(body['data'])

    def _profile(self, id_: str) -> Request:
        req = Request(
            'GET',
            'https://api.mercari.jp/users/get_profile',
            params={'user_id': id_, '_user_format': 'profile'},
            headers=self._headers,
        )
        return self._sign_request(req)
