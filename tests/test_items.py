import pytest


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_items(m):
    res = await m.items("362164700")
    assert res is not None

    assert len(res.items) == 30
    assert res.items[0].id_ == "m29374832086"
    assert res.items[0].name == "任天堂ライセンス商品 まるごと収納バッグ for Nintendo Switch"
    assert res.items[0].price == 1700
