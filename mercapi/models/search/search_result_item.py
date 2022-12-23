from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from mercapi.models import Item, Profile
from mercapi.models.base import Extractors, ResponseModel, ResponseProperty


class SearchResultItem(ResponseModel):
    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty("name", "name", Extractors.get("name")),
        ResponseProperty("price", "price", Extractors.get_as("price", int)),
    ]
    _optional_properties = [
        ResponseProperty("sellerId", "seller_id", Extractors.get("sellerId")),
        ResponseProperty("status", "status", Extractors.get("status")),
        ResponseProperty("created", "created", Extractors.get_datetime("created")),
        ResponseProperty("updated", "updated", Extractors.get_datetime("updated")),
        ResponseProperty("buyerId", "buyer_id", Extractors.get("buyerId")),
        ResponseProperty("thumbnails", "thumbnails", Extractors.get("thumbnails")),
        ResponseProperty("itemType", "item_type", Extractors.get("itemType")),
        ResponseProperty(
            "itemConditionId",
            "item_condition_id",
            Extractors.get_as("itemConditionId", int),
        ),
        ResponseProperty(
            "shippingPayerId",
            "shipping_payer_id",
            Extractors.get_as("shippingPayerId", int),
        ),
    ]

    def __init__(
        self,
        id_: str,
        name: str,
        price: int,
        seller_id: str,
        status: str,
        created: datetime,
        updated: datetime,
        buyer_id: str,
        thumbnails: List[str],
        item_type: str,
        item_condition_id: int,
        shipping_payer_id: int,
    ):
        super().__init__()
        self.id_ = id_
        self.name = name
        self.price = price
        self.seller_id = seller_id
        self.status = status
        self.created = created
        self.updated = updated
        self.buyer_id = buyer_id
        self.thumbnails = thumbnails
        self.item_type = item_type
        self.item_condition_id = item_condition_id
        self.shipping_payer_id = shipping_payer_id

    async def full_item(self) -> "Item":
        return await self._mercapi.item(self.id_)

    async def seller(self) -> "Profile":
        return await self._mercapi.profile(self.seller_id)
