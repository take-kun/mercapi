from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from mercapi.models.base import ResponseModel


@dataclass
class ProductDetail(ResponseModel):
    @dataclass
    class ShopStats(ResponseModel):
        shop_id: str
        score: int
        review_count: str

        @property
        def review_count_int(self) -> int:
            return int(self.review_count)

    @dataclass
    class ShopItem(ResponseModel):
        product_id: str
        display_name: str
        product_tags: list[str]
        thumbnail: str
        price: str

        @property
        def price_int(self) -> int:
            return int(self.price)

    @dataclass
    class Shop(ResponseModel):
        name: str
        display_name: str
        thumbnail: str
        shop_stats: "ProductDetail.ShopStats"
        allow_direct_message: bool
        shop_items: list["ProductDetail.ShopItem"]
        is_inbound_xb: bool

    @dataclass
    class Category(ResponseModel):
        category_id: str
        display_name: str
        parent_id: str
        root_id: str
        has_child: bool

    @dataclass
    class Brand(ResponseModel):
        brand_id: str
        display_name: str

    @dataclass
    class Condition(ResponseModel):
        display_name: str

    @dataclass
    class ShippingMethod(ResponseModel):
        shipping_method_id: str
        display_name: str
        is_anonymous: bool

    @dataclass
    class ShippingPayer(ResponseModel):
        shipping_payer_id: str
        display_name: str
        code: str

    @dataclass
    class ShippingDuration(ResponseModel):
        shipping_duration_id: str
        display_name: str
        min_days: int
        max_days: int

    @dataclass
    class ShippingFromArea(ResponseModel):
        shipping_area_code: str
        display_name: str

    @dataclass
    class ProductStats(ResponseModel):
        product_id: str
        score: int
        review_count: int
        likes_count: int

    @dataclass
    class Variant(ResponseModel):
        variant_id: str
        display_name: str
        quantity: str
        size: str

        @property
        def quantity_int(self) -> int:
            return int(self.quantity)

    shop: Shop
    photos: list[str]
    description: str
    categories: list[Category]
    brand: Brand
    condition: Condition
    shipping_method: ShippingMethod
    shipping_payer: ShippingPayer
    shipping_duration: ShippingDuration
    shipping_from_area: ShippingFromArea
    promotions: list[str]
    product_stats: ProductStats
    time_sale_details: Optional[str]  # TODO find example and provide typing
    variants: list[Variant]
    shipping_fee_config: Optional[str]  # TODO find example and provide typing
    variation_grouping: Optional[str]  # TODO find example and provide typing


@dataclass
class Product(ResponseModel):
    name: str
    display_name: str
    product_tags: list[str]
    thumbnail: str
    price: str
    create_time: datetime
    update_time: datetime
    attributes: list[str]
    product_detail: ProductDetail

    @property
    def price_int(self) -> int:
        return int(self.price)
