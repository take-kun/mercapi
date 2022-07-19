import json
import logging
import uuid

import httpx
from ecdsa import SigningKey, NIST256p

from mercapi.util import jwt

if __name__ == '__main__':
    requests = [
        ('categories.json', 'https://api.mercari.jp/master/get_item_categories'),
        ('brands.json', 'https://api.mercari.jp/master/get_item_brands'),
        ('sizes.json', 'https://api.mercari.jp/services/master/v1/itemSizes'),
        ('conditions.json', 'https://api.mercari.jp/services/master/v1/itemConditions'),
        ('shippingPayers.json', 'https://api.mercari.jp/services/master/v1/shippingPayers'),
        ('colors.json', 'https://api.mercari.jp/services/master/v1/itemColors'),
        ('shippingMethods.json', 'https://api.mercari.jp/services/master/v1/shippingMethods'),
    ]

    url = 'https://api.mercari.jp/master/get_item_categories'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'
    key = SigningKey.generate(NIST256p)

    uuid_ = str(uuid.uuid4())
    for output, url in requests:
        r = httpx.get(
            url,
            headers={
                'User-Agent': user_agent,
                'X-Platform': 'web',
                'DPoP': jwt.generate_dpop(url, 'GET', key, {'uuid': uuid_}),
            }
        )
        if r.is_error:
            logging.error(f'Request for {output} failed')
            logging.error(r)
        with open(output, 'w', encoding='utf8') as file:
            json.dump(r.json(), file, ensure_ascii=False, indent=4)
