import pytest


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_profile(m):
    res = await m.profile("362164700")
    assert res is not None

    assert res.name == "nananao"
