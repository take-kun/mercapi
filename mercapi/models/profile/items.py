from dataclasses import dataclass
from datetime import datetime
from typing import List

from mercapi.models.base import ResponseModel
from mercapi.models.common import ItemCategory
from mercapi.models.item.data import ShippingFromArea
from mercapi.models import Item


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

    async def full_item(self) -> Item:
        """Fetch full details of a listing (item).

        Equivalent of :func:`~mercapi.Mercapi.item`
        """
        return await self._mercapi.item(self.id_)


@dataclass
class Items(ResponseModel):
    items: List[SellerItem]
