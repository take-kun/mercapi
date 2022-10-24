import uuid
from dataclasses import dataclass, field
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

    @dataclass
    class SearchConditions:
        query: str
        categories: List[int] = field(default_factory=list)
        brands: List[int] = field(default_factory=list)
        sizes: List[int] = field(default_factory=list)
        price_min: int = 0
        price_max: int = 0
        item_conditions: List[int] = field(default_factory=list)
        shipping_payer: List[int] = field(default_factory=list)
        colors: List[int] = field(default_factory=list)
        shipping_methods: List["SearchRequestData.ShippingMethod"] = field(
            default_factory=list
        )
        status: List["SearchRequestData.Status"] = field(default_factory=list)

    def __init__(self, search_conditions: SearchConditions):
        super().__init__()
        (
            query,
            categories,
            brands,
            sizes,
            price_min,
            price_max,
            item_conditions,
            shipping_payer,
            colors,
        ) = map(
            search_conditions.__dict__.get,
            (
                "query",
                "categories",
                "brands",
                "sizes",
                "price_min",
                "price_max",
                "item_categories",
                "shipping_payer",
                "colors",
            ),
        )
        shipping_methods = [i.name for i in search_conditions.shipping_methods]
        status = [i.name for i in search_conditions.status]
        if "STATUS_SOLD_OUT" in status:
            status.extend("STATUS_TRADING")

        self.data = {
            "userId": "",
            "pageSize": 120,
            "pageToken": "",
            "searchSessionId": uuid.uuid4().hex,
            "indexRouting": "INDEX_ROUTING_UNSPECIFIED",
            "thumbnailTypes": [],
            "searchCondition": {
                "keyword": query,
                "excludeKeyword": "",
                "sort": "SORT_SCORE",
                "order": "ORDER_DESC",
                "status": [],
                "sizeId": sizes,
                "categoryId": categories,
                "brandId": brands,
                "sellerId": [],
                "priceMin": price_min,
                "priceMax": price_max,
                "itemConditionId": item_conditions,
                "shippingPayerId": shipping_payer,
                "shippingFromArea": [],
                "shippingMethod": shipping_methods,
                "colorId": colors,
                "hasCoupon": False,
                "attributes": [],
                "itemTypes": [],
                "skuIds": [],
            },
            "defaultDatasets": [],
            "serviceFrom": "suruga",
        }
