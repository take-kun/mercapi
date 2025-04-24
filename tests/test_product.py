from datetime import datetime, timezone

import pytest


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_product(m):
    res = await m.product("uU4Ahinr6rGNFLNYQpa9E7")
    assert res is not None

    assert res.name == "uU4Ahinr6rGNFLNYQpa9E7"
    assert (
        res.display_name == "【PS2】Beatmania ⅡDX 16 EMPRESS + PREMIUM BEST ソフトのみ ビートマニア"
    )
    assert res.product_tags == []
    assert (
        res.thumbnail
        == "https://assets.mercari-shops-static.com/-/small/plain/5VX9LCnEfBdm3hvv97sAXT.jpg@jpg"
    )
    assert res.price == "6300"
    assert res.create_time == datetime(2025, 4, 15, 14, 9, 35, tzinfo=timezone.utc)
    assert res.update_time == datetime(2025, 4, 21, 4, 49, 54, tzinfo=timezone.utc)
    assert res.attributes == []

    detail = res.product_detail
    assert detail.shop.name == "wkkCxHU3Rx8WqyZ77YgMaF"
    assert detail.shop.display_name == "直江堂@タイムセール商品は同梱不可"
    assert (
        detail.shop.thumbnail
        == "https://assets.mercari-shops-static.com/-/small/plain/bj8nXES3x7KFcGRJqeZrD6.jpg@jpg"
    )
    assert detail.shop.allow_direct_message is True
    assert detail.shop.is_inbound_xb is False

    shop_stats = detail.shop.shop_stats
    assert shop_stats.shop_id == "wkkCxHU3Rx8WqyZ77YgMaF"
    assert shop_stats.score == 5
    assert shop_stats.review_count == "7437"

    assert len(detail.shop.shop_items) == 6
    shop_item = detail.shop.shop_items[0]
    assert shop_item.product_id == "Qv25jGNXs8rvT5mBiX5RD"
    assert shop_item.display_name == "SDBBショップ様専用"
    assert shop_item.product_tags == ["sold_out"]
    assert (
        shop_item.thumbnail
        == "https://assets.mercari-shops-static.com/-/small/plain/x2C6aGnE8LTzzSreTdrtAe.jpg@jpg"
    )
    assert shop_item.price == "3100"

    assert detail.photos == [
        "https://assets.mercari-shops-static.com/-/large/plain/5VX9LCnEfBdm3hvv97sAXT.jpg@jpg",
        "https://assets.mercari-shops-static.com/-/large/plain/ksZGwqpDmyFfYZTGDcWDTK.jpg@jpg",
        "https://assets.mercari-shops-static.com/-/large/plain/DaTyMLx7at6i2qZ94kZ6bB.jpg@jpg",
    ]
    assert (
        detail.description
        == "動作確認済み。ソフトのみ\n\n緩衝材なしの梱包となります(希望されても入れる事は出来ません)\n\n中古品の為プロダクトコード等は全て使用済みとお考え下さい。\n\n同梱を希望される方は+1品につき200円お値引きさせて頂きますので、購入前に質問にてお願いします。\n(但し、お値引は+3品までとなります)\n\n基本的には無言取引で取引メッセージは何かトラブルや要望があった場合のみ対応します。\n\n#直江堂"
    )

    assert len(detail.categories) == 5
    category = detail.categories[0]
    assert category.category_id == "7145"
    assert category.display_name == "ソフト"
    assert category.parent_id == "7136"
    assert category.root_id == "1328"
    assert category.has_child is False

    assert detail.brand.brand_id == "3267"
    assert detail.brand.display_name == "プレイステーション2"

    assert detail.condition.display_name == "やや傷や汚れあり"

    assert detail.shipping_method.shipping_method_id == "3"
    assert detail.shipping_method.display_name == "らくらくメルカリ便"
    assert detail.shipping_method.is_anonymous is True

    assert detail.shipping_payer.shipping_payer_id == "1"
    assert detail.shipping_payer.display_name == "送料込み(出品者負担)"
    assert detail.shipping_payer.code == "SELLER"

    assert detail.shipping_duration.shipping_duration_id == "2"
    assert detail.shipping_duration.display_name == "2〜3日で発送"
    assert detail.shipping_duration.min_days == 2
    assert detail.shipping_duration.max_days == 3

    assert detail.shipping_from_area.shipping_area_code == "jp33"
    assert detail.shipping_from_area.display_name == "岡山県"

    stats = detail.product_stats
    assert stats.product_id == "uU4Ahinr6rGNFLNYQpa9E7"
    assert stats.score == 0
    assert stats.review_count == 0
    assert stats.likes_count == 1

    assert len(detail.variants) == 1
    variant = detail.variants[0]
    assert variant.variant_id == "VmcgXM63ZjRAQdzxi4X8Ja"
    assert variant.display_name == ""
    assert variant.quantity == "1"
    assert variant.size == ""
