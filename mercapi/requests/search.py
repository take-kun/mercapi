import uuid
from enum import Enum
from typing import List

from mercapi.requests import RequestData


class SearchRequestData(RequestData):
    class ShippingMethod(Enum):
        SHIPPING_METHOD_ANONYMOUS = 1
        SHIPPING_METHOD_JAPAN_POST = 2
        SHIPPING_METHOD_NO_OPTION = 3

    class Status(Enum):
        STATUS_ON_SALE = 1
        STATUS_SOLD_OUT = 2
        # STATUS_TRADING = 3

    def __init__(self, query: str, categories: List[int] = [], brands: List[int] = [], sizes: List[int] = [],
                 price_min: int = None, price_max: int = None, item_conditions: List[int] = [],
                 shipping_payer: List[int] = [], colors: List[int] = [], shipping_methods: List[ShippingMethod] = [],
                 status: List[Status] = []):
        super().__init__()
        if price_min is None:
            price_min = 0
        if price_max is None:
            price_max = 0
        if shipping_methods:
            shipping_methods = [i.name for i in shipping_methods]
        if status:
            status = [i.name for i in status]
            if 'STATUS_SOLD_OUT' in status:
                status.extend('STATUS_TRADING')

        self.data = {"userId": "", "pageSize": 120, "pageToken": "", "searchSessionId": uuid.uuid4().hex,
                     "indexRouting": "INDEX_ROUTING_UNSPECIFIED", "thumbnailTypes": [],
                     "searchCondition": {"keyword": query, "excludeKeyword": "", "sort": "SORT_SCORE",
                                         "order": "ORDER_DESC", "status": [], "sizeId": sizes, "categoryId": categories,
                                         "brandId": brands, "sellerId": [], "priceMin": price_min,
                                         "priceMax": price_max, "itemConditionId": item_conditions,
                                         "shippingPayerId": shipping_payer, "shippingFromArea": [],
                                         "shippingMethod": shipping_methods, "colorId": colors, "hasCoupon": False,
                                         "attributes": [], "itemTypes": [], "skuIds": []},
                     "defaultDatasets": [], "serviceFrom": "suruga"}
