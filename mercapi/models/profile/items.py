from dataclasses import dataclass
from datetime import datetime
from typing import List

from mercapi.models.base import ResponseModel
from mercapi.models.common import ItemCategory
from mercapi.models.item.data import ShippingFromArea


@dataclass
class SellerItem(ResponseModel):
    id_: str
    seller_id: str
    status: str
    name: str
    price: int
    thumbnails: List[str]
    root_category_id: int
    num_likes: int
    num_comments: int
    created: datetime
    updated: datetime
    item_category: ItemCategory
    shipping_from_area: ShippingFromArea


@dataclass
class Items(ResponseModel):
    items: List[SellerItem]
