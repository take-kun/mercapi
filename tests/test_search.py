import pytest

from mercapi import mercapi
from tests import my_vcr


m = mercapi.Mercapi()


@pytest.mark.asyncio
@my_vcr.use_cassette()
async def test_simple_search_query():
    res = await m.search('sharpnel')
    assert len(res.items) == 106

    item = res.items[0]
    assert item.name == '【廃盤】DJ SHARPNEL シャープネルサウンドコレクション壱'
    assert item.price == 9444
    assert item.status == 'ITEM_STATUS_ON_SALE'
