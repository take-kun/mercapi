import uuid

from mercapi.requests import RequestData


class SearchRequestData(RequestData):
    def __init__(self, query: str):
        super().__init__()
        self.data = {"userId": "", "pageSize": 120, "pageToken": "", "searchSessionId": uuid.uuid4().hex,
                     "indexRouting": "INDEX_ROUTING_UNSPECIFIED", "thumbnailTypes": [],
                     "searchCondition": {"keyword": query, "excludeKeyword": "", "sort": "SORT_SCORE",
                                         "order": "ORDER_DESC", "status": [], "sizeId": [], "categoryId": [],
                                         "brandId": [],
                                         "sellerId": [], "priceMin": 0, "priceMax": 0, "itemConditionId": [],
                                         "shippingPayerId": [], "shippingFromArea": [], "shippingMethod": [],
                                         "colorId": [],
                                         "hasCoupon": False, "attributes": [], "itemTypes": [], "skuIds": []},
                     "defaultDatasets": [], "serviceFrom": "suruga"}
