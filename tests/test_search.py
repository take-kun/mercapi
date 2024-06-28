from datetime import datetime

import pytest

from mercapi.util.errors import IncorrectRequestError
from mercapi.requests import SearchRequestData


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_simple_search_query(m):
    res = await m.search("完全網羅は無理でしたMix", categories=[75])
    assert len(res.items) == 2
    assert res.meta.num_found == 2

    item = res.items[0]
    assert item.id_ == "m94786104879"
    assert item.seller_id == "362164700"
    assert item.status == "ITEM_STATUS_ON_SALE"
    assert item.name == "DJ Sharpnel　完全網羅は無理でしたMix"
    assert item.price == 4800
    assert int(datetime.timestamp(item.created)) == 1652715351
    assert int(datetime.timestamp(item.updated)) == 1661206795
    assert len(item.thumbnails) == 1
    assert (
        item.thumbnails[0]
        == "https://static.mercdn.net/c!/w=240,f=webp/thumb/photos/m94786104879_1.jpg?1652715351"
    )
    assert item.item_type == "ITEM_TYPE_MERCARI"
    assert item.item_condition_id == 3
    assert item.shipping_payer_id == 2


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
    res = await m.search("完全網羅は無理でしたMix", categories=[75])
    item = res.items[0]

    full_item = await item.full_item()
    assert full_item.id_ == "m94786104879"


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_fetch_next_page(m):
    res = await m.search("sharpnel")
    res = await res.next_page()
    item = res.items[0]

    assert item.id_ == "m49788155901"
    assert item.name == "beatmania IIDX 28 BISTROVER サウンドトラック"


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_fetch_prev_page(m):
    res = await m.search("sharpnel", page_token="v1:1")
    res = await res.prev_page()
    item = res.items[0]

    assert item.id_ == "m93879216403"
    assert item.name == "DJ Sharpnel  アニメガバイト プレス版"


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_fetch_prev_page_on_first_page(m):
    res = await m.search("sharpnel")
    with pytest.raises(IncorrectRequestError):
        await res.prev_page()


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_fetch_next_page_on_last_page(m):
    res = await m.search("sharpnel mad breaks")
    with pytest.raises(IncorrectRequestError):
        await res.next_page()


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_sort_by_price_asc(m):
    res = await m.search(
        "sharpnel",
        sort_by=SearchRequestData.SortBy.SORT_PRICE,
        sort_order=SearchRequestData.SortOrder.ORDER_ASC,
    )
    prices = [i.price for i in res.items]

    for a, b in zip(prices, prices[1:]):
        assert a <= b


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_exclude_keywords(m):
    res = await m.search("sharpnel", exclude="beatmania")
    assert all("beatmania" not in i.name.lower() for i in res.items)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_filter_by_status_on_sale(m):
    res = await m.search("sharpnel", status=[SearchRequestData.Status.STATUS_ON_SALE])
    assert all(i.status == "ITEM_STATUS_ON_SALE" for i in res.items)
