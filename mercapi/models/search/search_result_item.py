from dataclasses import dataclass
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from mercapi.models import Item, Profile
from mercapi.models.base import ResponseModel


@dataclass
class SearchResultItem(ResponseModel):
    id_: str
    name: str
    price: int
    seller_id: str
    status: str
    created: datetime
    updated: datetime
    thumbnails: List[str]
    item_type: str
    item_condition_id: int
    shipping_payer_id: int

    async def full_item(self) -> "Item":
        return await self._mercapi.item(self.id_)

    async def seller(self) -> "Profile":
        return await self._mercapi.profile(self.seller_id)
