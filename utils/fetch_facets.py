import json
import logging
import os
import uuid
from pathlib import Path

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
            logging.error(f'Request for {url} failed')
            logging.error(r)

        cwd = os.path.abspath(os.path.dirname(__file__))  # assuming script runs in 'mercapi/utils'
        output_dir = Path(cwd).parent / 'docs' / 'facets'
        if not output_dir.is_dir():
            output_dir.mkdir()
        with open(output_dir / output, 'w', encoding='utf8') as file:
            json.dump(r.json(), file, ensure_ascii=False, indent=4)
