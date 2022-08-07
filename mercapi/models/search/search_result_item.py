from datetime import datetime
from typing import List

from mercapi.models import ResponseModel
from mercapi.models.base import Extractors


class SearchResultItem(ResponseModel):
    _required_properties = [
        ('id', 'id_', Extractors.get('id')),
        ('name', 'name', Extractors.get('name')),
        ('price', 'price', Extractors.get_as('price', int)),
    ]
    _optional_properties = [
        ('sellerId', 'seller_id', Extractors.get('sellerId')),
        ('status', 'status', Extractors.get('status')),
        ('created', 'created', Extractors.get_datetime('created')),
        ('updated', 'updated', Extractors.get_datetime('updated')),
        ('buyerId', 'buyer_id', Extractors.get('buyerId')),
        ('thumbnails', 'thumbnails', Extractors.get('thumbnails')),
        ('itemType', 'item_type', Extractors.get('itemType')),
        ('itemConditionId', 'item_condition_id', Extractors.get_as('itemConditionId', int)),
        ('shippingPayerId', 'shipping_payer_id', Extractors.get_as('shippingPayerId', int)),
    ]

    def __init__(self, id_: str, name: str, price: int, seller_id: str, status: str, created: datetime,
                 updated: datetime, buyer_id: str, thumbnails: List[str], item_type: str, item_condition_id: int,
                 shipping_payer_id: int):
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
