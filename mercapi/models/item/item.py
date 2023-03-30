from dataclasses import dataclass
from datetime import datetime
from typing import List

from mercapi.models.base import ResponseModel
from mercapi.models.common import ItemCategorySummary
from mercapi.models.item.data import (
    ItemCondition,
    ShippingFromArea,
    ShippingMethod,
    ShippingDuration,
    ShippingClass,
    ShippingPayer,
    Color,
    Seller,
    Comment,
)


# actually a mapping for 'data' object in item response
#
# consider nesting all the properties in data submodel
# if the original response gets more verbose
@dataclass
class Item(ResponseModel):
    id_: str
    seller: Seller
    status: str
    name: str
    price: int
    description: str
    photos: List[str]
    photo_paths: List[str]
    thumbnails: List[str]
    item_category: ItemCategorySummary
    item_condition: ItemCondition
    colors: List[Color]
    shipping_payer: ShippingPayer
    shipping_method: ShippingMethod
    shipping_from_area: ShippingFromArea
    shipping_duration: ShippingDuration
    shipping_class: ShippingClass
    num_likes: int
    num_comments: int
    comments: List[Comment]
    updated: datetime
    created: datetime
    pager_id: int
    liked: bool
    checksum: str
    is_dynamic_shipping_fee: bool
    application_attributes: dict
    is_shop_item: str
    is_anonymous_shipping: bool
    is_web_visible: bool
    is_offerable: bool
    is_organizational_user: bool
    organizational_user_status: str
    is_stock_item: bool
    is_cancelable: bool
    shipped_by_worker: bool
    has_additional_service: bool
    has_like_list: bool
    is_offerable_v2: bool
