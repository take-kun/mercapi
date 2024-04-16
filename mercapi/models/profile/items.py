from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from mercapi.models import Item
from mercapi.models.base import ResponseModel
from mercapi.models.common import ItemCategorySummary
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
    item_category: Optional[ItemCategorySummary]
    shipping_from_area: ShippingFromArea

    async def full_item(self) -> Item:
        """Fetch full details of a listing (item).

        Equivalent of :func:`~mercapi.Mercapi.item`
        """
        return await self._mercapi.item(self.id_)


@dataclass
class Items(ResponseModel):
    items: List[SellerItem]
