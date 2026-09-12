from datetime import datetime

import pytest


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_items(m):
    res = await m.items("362164700")
    assert res is not None

    assert len(res.items) == 30

    item = res.items[0]
    assert item.id_ == "m50109631296"
    assert item.name == "ワークマン 防水エアロゲル JETキャップ 59cm ブラック ゴルフ"
    assert item.price == 1600
    assert item.thumbnails == [
        "https://static.mercdn.net/thumb/item/jpeg/m50109631296_1.jpg?1771575495"
    ]
    assert item.root_category_id == 0
    assert item.num_likes == 0
    assert item.num_comments == 0
    assert int(datetime.timestamp(item.created)) == 1771575495
    assert int(datetime.timestamp(item.updated)) == 1771575495

    shipping_from_area = item.shipping_from_area
    assert shipping_from_area.id_ == 10
    assert shipping_from_area.name == "群馬県"


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_items_fetch_full_item_from_seller_item(m):
    items = await m.items("362164700")
    res = await items.items[0].full_item()

    assert res.id_ == "m50109631296"
