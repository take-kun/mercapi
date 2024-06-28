from dataclasses import dataclass
from datetime import datetime
from typing import List, TYPE_CHECKING, Optional

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
    shipping_method_id: int
    category_id: int
    is_no_price: bool  # price==9999999 if True

    async def full_item(self) -> "Item":
        return await self._mercapi.item(self.id_)

    async def seller(self) -> "Profile":
        return await self._mercapi.profile(self.seller_id)

    """
    Actual price of the item, properly handling the case when the item has no price.
    """

    @property
    def real_price(self) -> Optional[int]:
        return None if self.is_no_price else self.price
