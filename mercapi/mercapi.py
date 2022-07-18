import random
import uuid
from typing import Optional

import httpx
from ecdsa import SigningKey, NIST256p
from httpx import Request

from mercapi.models import SearchResults, Item
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

    async def search(self, query: str) -> SearchResults:
        res = await self._client.send(self._search(query))
        body = res.json()
        return SearchResults.from_dict(body)

    def _search(self, query: str) -> Request:
        data = SearchRequestData(query)
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
