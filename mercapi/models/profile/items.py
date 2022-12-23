from datetime import datetime
from typing import List

from mercapi.models.base import Extractors, ResponseModel, ResponseProperty
from mercapi.models.common import ItemCategory
from mercapi.models.item.data import ShippingFromArea


class SellerItem(ResponseModel):
    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty(
            "seller",
            "seller_id",
            Extractors.get_with(
                "seller_id", lambda x: str(x["id"]) if "id" in x else None
            ),
        ),
        ResponseProperty("status", "status", Extractors.get("status")),
        ResponseProperty("name", "name", Extractors.get("name")),
        ResponseProperty("price", "price", Extractors.get("price")),
    ]
    _optional_properties = [
        ResponseProperty("thumbnails", "thumbnails", Extractors.get("thumbnails")),
        ResponseProperty(
            "root_category_id", "root_category_id", Extractors.get("root_category_id")
        ),
        ResponseProperty("num_likes", "num_likes", Extractors.get("num_likes")),
        ResponseProperty(
            "num_comments", "num_comments", Extractors.get("num_comments")
        ),
        ResponseProperty("created", "created", Extractors.get_datetime("created")),
        ResponseProperty("updated", "updated", Extractors.get_datetime("updated")),
        ResponseProperty(
            "item_category",
            "item_category",
            Extractors.get_as_model("item_category", ItemCategory),
        ),
        ResponseProperty(
            "shipping_from_area",
            "shipping_from_area",
            Extractors.get_as_model("shipping_from_area", ShippingFromArea),
        ),
    ]

    def __init__(
        self,
        id_: str,
        seller_id: str,
        status: str,
        name: str,
        price: int,
        thumbnails: List[str],
        root_category_id: int,
        num_likes: int,
        num_comments: int,
        created: datetime,
        updated: datetime,
        item_category: ItemCategory,
        shipping_from_area: ShippingFromArea,
    ):
        self.id_ = id_
        self.seller_id = seller_id
        self.status = status
        self.name = name
        self.price = price
        self.thumbnails = thumbnails
        self.root_category_id = root_category_id
        self.num_likes = num_likes
        self.num_comments = num_comments
        self.created = created
        self.updated = updated
        self.item_category = item_category
        self.shipping_from_area = shipping_from_area


class Items(ResponseModel):
    _required_properties = [
        ResponseProperty(
            "data", "items", Extractors.get_list_of_model("data", SellerItem)
        ),
    ]
    _optional_properties = []

    def __init__(self, items: List[SellerItem]):
        super().__init__()
        self.items = items
