from datetime import datetime

import pytest


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_items(m):
    res = await m.items("362164700")
    assert res is not None

    assert len(res.items) == 30

    item = res.items[0]
    assert item.id_ == "m62857872792"
    assert item.name == "Reminiscences しんたろーアートワークス 画集 イラスト"
    assert item.price == 1600
    assert item.thumbnails == [
        "https://static.mercdn.net/c!/w=240/thumb/photos/m62857872792_1.jpg?1663161407"
    ]
    assert item.root_category_id == 5
    assert item.num_likes == 0
    assert item.num_comments == 0
    assert int(datetime.timestamp(item.created)) == 1663161407
    assert int(datetime.timestamp(item.updated)) == 1663161407

    item_category = item.item_category
    assert item_category.id_ == 677
    assert item_category.name == "アート/エンタメ"
    assert item_category.parent_category_id == 72
    assert item_category.parent_category_name == "本"
    assert item_category.root_category_id == 5
    assert item_category.root_category_name == "本・音楽・ゲーム"

    shipping_from_area = item.shipping_from_area
    assert shipping_from_area.id_ == 20
    assert shipping_from_area.name == "長野県"


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_items_fetch_full_item_from_seller_item(m):
    items = await m.items("362164700")
    res = await items.items[0].full_item()

    assert res.id_ == "m77200069010"
