import logging
from datetime import datetime
from typing import List

from mercapi.models import ResponseModel
from mercapi.util.errors import ParseAPIResponseError


class SearchResultItem(ResponseModel):
    def __init__(self, id_: str, name: str, price: int, seller_id: str,
                 status: str, created: datetime, updated: datetime,
                 buyer_id: str, thumbnails: List[str], item_type: str,
                 item_condition_id: int, shipping_payer_id: int):
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

    def __repr__(self):
        return f'{__name__}.{self.__class__} - id={self.id_}, price={self.price}'

    @classmethod
    def from_dict(cls, d: dict):
        model_dict_required_map = {
            'id_': lambda x: x.get('id'),
            'name': lambda x: x.get('name'),
            'price': lambda x: int(x.get('price')),
        }
        model_dict_optional_map = {
            'seller_id': lambda x: x.get('sellerId'),
            'status': lambda x: x.get('status'),
            'created': lambda x: datetime.utcfromtimestamp(float(x.get('created'))),
            'updated': lambda x: datetime.utcfromtimestamp(float(x.get('updated'))),
            'buyer_id': lambda x: x.get('buyerId'),
            'thumbnails': lambda x: x.get('thumbnails'),
            'item_type': lambda x: x.get('itemType'),
            'item_condition_id': lambda x: x.get('itemConditionId'),
            'shipping_payer_id': lambda x: x.get('shippingPayerId'),
        }

        properties = {}
        for prop, func in model_dict_required_map.items():
            try:
                properties[prop] = func(d)
            except Exception as e:
                raise ParseAPIResponseError(
                    f'Failed to retrieve required SearchResult property {prop} from the response'
                ) from e

        for prop, func in model_dict_optional_map.items():
            val = None
            try:
                val = func(d)
            except Exception as e:
                logging.warning(f'Failed to retrieve SearchResult property {prop} from the response. ' +
                                'See the reason in debug.')
                logging.debug(e)
            properties[prop] = val

        return SearchResultItem(**properties)

    def as_dict(self) -> dict:
        return vars(self)
