import pytest


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_simple_search_query(m):
    res = await m.search("sharpnel")
    assert len(res.items) == 106

    item = res.items[0]
    assert item.name == "【廃盤】DJ SHARPNEL シャープネルサウンドコレクション壱"
    assert item.price == 9444
    assert item.status == "ITEM_STATUS_ON_SALE"

    assert res.meta.num_found == 111


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_with_item_condition_filter(m):
    res = await m.search("sharpnel", item_conditions=[2])
    assert [i.item_condition_id == 2 for i in res.items]


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_with_shipping_payer_filter(m):
    res = await m.search("sharpnel", shipping_payer=[2])
    assert [i.shipping_payer_id == 2 for i in res.items]


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_with_min_price_filter(m):
    res = await m.search("sharpnel", price_min=5000)
    assert [i.price >= 5000 for i in res.items]


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_with_max_price_filter(m):
    res = await m.search("sharpnel", price_max=5000)
    assert [i.price <= 5000 for i in res.items]


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_with_min_price_and_max_price_filter(m):
    res = await m.search("sharpnel", price_min=5000, price_max=10000)
    assert [5000 <= i.price <= 10000 for i in res.items]


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_fetch_full_item_from_result(m):
    res = await m.search("sharpnel")
    item = res.items[0]

    full_item = await item.full_item()
    assert full_item.id_ == "m29475719206"
