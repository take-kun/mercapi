from datetime import datetime

import pytest


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_profile(m):
    res = await m.profile("362164700")
    assert res is not None

    assert res.name == "nananao"
    assert res.id_ == 362164700
    assert res.photo_url == "https://static.mercdn.net/images/member_photo_noimage.png"
    assert (
        res.photo_thumbnail_url
        == "https://static.mercdn.net/images/member_photo_noimage_thumb.png"
    )
    assert res.register_sms_confirmation == "yes"
    assert res.ratings.good == 1049
    assert res.ratings.normal == 3
    assert res.ratings.bad == 0
    assert res.polarized_ratings.good == 1052
    assert res.polarized_ratings.bad == 0
    assert res.num_ratings == 1052
    assert res.star_rating_score == 5
    assert res.is_followable is True
    assert res.is_blocked is False
    assert res.following_count == 0
    assert res.follower_count == 10
    assert res.score == 1049
    assert int(datetime.timestamp(res.created)) == 1521901729
    assert res.proper is True
    assert (
        res.introduction
        == "発送まで1週間ほどお時間をいただく場合もあります。\r\n梱包材は再利用品です。\r\n発送方法や早めは希望があればご相談下さい。\r\n撮影や確認など手間のかかる事はお断りする事もあります。\r\nお取引にて至らない点もありますがよろしくお願い致します。"
    )
    assert res.is_official is False
    assert res.num_sell_items == 578
    assert res.num_ticket == 0
    assert res.bounce_mail_flag == "no"
    assert res.current_point == 0
    assert res.current_sales == 0
    assert res.is_organizational_user is False
