import logging
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any

from mercapi.requests import RequestData

log = logging.getLogger(__name__)


@dataclass
class SearchRequestData(RequestData):
    class ShippingMethod(Enum):
        SHIPPING_METHOD_ANONYMOUS = 1
        SHIPPING_METHOD_JAPAN_POST = 2
        SHIPPING_METHOD_NO_OPTION = 3

    class Status(Enum):
        STATUS_ON_SALE = 1
        STATUS_SOLD_OUT = 2
        # STATUS_TRADING = 3

    class SortBy(Enum):
        SORT_SCORE = 1
        SORT_CREATED_TIME = 2  # Correct order is not guaranteed
        SORT_PRICE = 3
        SORT_NUM_LIKES = 4

    class SortOrder(Enum):
        ORDER_DESC = 1
        ORDER_ASC = 2

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
        sort_by: "SearchRequestData.SortBy" = 1
        sort_order: "SearchRequestData.SortOrder" = 1
        exclude: str = ""

    search_conditions: SearchConditions
    page_token: str = ""

    _allowed_sorting = [
        (SortBy.SORT_SCORE, SortOrder.ORDER_DESC),
        (SortBy.SORT_CREATED_TIME, SortOrder.ORDER_DESC),
        (SortBy.SORT_PRICE, SortOrder.ORDER_DESC),
        (SortBy.SORT_PRICE, SortOrder.ORDER_ASC),
        (SortBy.SORT_NUM_LIKES, SortOrder.ORDER_DESC),
    ]

    @property
    def data(self) -> Dict[str, Any]:
        shipping_methods = [i.name for i in self.search_conditions.shipping_methods]
        status = [i.name for i in self.search_conditions.status]
        if "STATUS_SOLD_OUT" in status:
            status.extend(["STATUS_TRADING"])

        if (
            self.search_conditions.sort_by,
            self.search_conditions.sort_order,
        ) not in self._allowed_sorting:
            log.warning(
                f"Parameter {self.search_conditions.sort_by} used in conjugation with "
                f"{self.search_conditions.sort_order} is not supported by the official web-app. Proceed with caution."
            )

        return {
            "userId": "",
            "pageSize": 120,
            "pageToken": self.page_token,
            "searchSessionId": uuid.uuid4().hex,
            "indexRouting": "INDEX_ROUTING_UNSPECIFIED",
            "thumbnailTypes": [],
            "searchCondition": {
                "keyword": self.search_conditions.query,
                "sort": self.search_conditions.sort_by.name,
                "order": self.search_conditions.sort_order.name,
                "status": status,
                "sizeId": self.search_conditions.sizes,
                "categoryId": self.search_conditions.categories,
                "brandId": self.search_conditions.brands,
                "sellerId": [],
                "priceMin": self.search_conditions.price_min,
                "priceMax": self.search_conditions.price_max,
                "itemConditionId": self.search_conditions.item_conditions,
                "shippingPayerId": self.search_conditions.shipping_payer,
                "shippingFromArea": [],
                "shippingMethod": shipping_methods,
                "colorId": self.search_conditions.colors,
                "hasCoupon": False,
                "attributes": [],
                "itemTypes": [],
                "skuIds": [],
                "excludeKeyword": self.search_conditions.exclude,
            },
            "defaultDatasets": [],
            "serviceFrom": "suruga",
        }
