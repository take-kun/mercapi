from datetime import datetime

import pytest


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_item(m):
    res = await m.item("m12871737078")
    assert res is not None

    assert res.id_ == "m12871737078"
    assert res.name == "DJ Sharpnel / PPPH!"
    assert res.price == 8000
    assert res.status == "sold_out"
    assert res.description == "DJ Sharpnel\nPPPH! -Phat, Pinky, Powerful & Hard!!-\n\n名作ですね…(CD-R盤)\n\nDJ Sharpnel\nナードコア"
    assert res.photos == [
        "https://static.mercdn.net/item/detail/orig/photos/m12871737078_1.jpg?1654847197",
        "https://static.mercdn.net/item/detail/orig/photos/m12871737078_2.jpg?1654847197",
        "https://static.mercdn.net/item/detail/orig/photos/m12871737078_3.jpg?1654847197",
        "https://static.mercdn.net/item/detail/orig/photos/m12871737078_4.jpg?1654847197"
    ]
    assert res.photo_paths == [
        "photos/m12871737078_1.jpg",
        "photos/m12871737078_2.jpg",
        "photos/m12871737078_3.jpg",
        "photos/m12871737078_4.jpg"
    ]
    assert res.thumbnails == [
        "https://static.mercdn.net/c!/w=240/thumb/photos/m12871737078_1.jpg?1654847197"
    ]
    assert res.num_likes == 1
    assert res.num_comments == 0
    assert res.comments == []
    assert int(datetime.timestamp(res.updated)) == 1656584699
    assert int(datetime.timestamp(res.created)) == 1654847197
    assert res.pager_id == 5385007574
    assert res.checksum == "486cd636c6ee86e575fdf051c8eeda9b"
    assert res.is_dynamic_shipping_fee is False
    assert res.application_attributes == {}
    assert res.is_shop_item == "no"
    assert res.is_anonymous_shipping is True
    assert res.is_web_visible is True
    assert res.is_offerable is False
    assert res.is_organizational_user is False
    assert res.organizational_user_status == ""
    assert res.is_stock_item is False
    assert res.is_cancelable is True
    assert res.shipped_by_worker is False
    assert res.has_additional_service is False
    assert res.has_like_list is False
    assert res.is_offerable_v2 is False

    seller = res.seller
    assert seller.id_ == 485869194
    assert seller.name == "adieusos"
