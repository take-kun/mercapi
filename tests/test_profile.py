import pytest

from conftest import my_vcr


@pytest.mark.asyncio
@my_vcr.use_cassette()
async def test_profile(m):
    res = await m.profile('362164700')
    assert res is not None

    assert res.name == 'nananao'
