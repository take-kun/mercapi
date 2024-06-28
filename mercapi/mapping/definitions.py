import logging
from datetime import datetime
from typing import NamedTuple, List, Dict, TypeVar, Type, Any, Optional, Callable

from mercapi.models import Item, Items, Profile, SearchResults, SearchResultItem
from mercapi.models.common import ItemCategory, ItemCategorySummary
from mercapi.models.item.data import (
    Seller,
    ItemCondition,
    Color,
    ShippingPayer,
    ShippingMethod,
    ShippingFromArea,
    ShippingDuration,
    ShippingClass,
    Comment,
)
from mercapi.util.errors import ParseAPIResponseError
from mercapi.models.base import ResponseModel
from mercapi.models.profile.items import SellerItem
from mercapi.models.search import Meta

T = TypeVar("T")
ExtractorDef = Callable[[dict], Optional[T]]


class ResponseProperty(NamedTuple):
    raw_property_name: str
    model_property_name: str
    extractor: ExtractorDef


class ResponseMappingDefinition(NamedTuple):
    required_properties: List[ResponseProperty]
    optional_properties: List[ResponseProperty]


class Extractors:
    """
    Collection of HOFs for parsing API responses in the most common ways.

    Each extractor function MUST handle lack of requested key
    in the response object (dict) and return None in such cases.
    """

    @staticmethod
    def get(key: str) -> ExtractorDef[Any]:
        return lambda x: x.get(key)

    S = TypeVar("S", int, float, str)

    @staticmethod
    def get_as(key: str, type_: Type[S]) -> ExtractorDef[S]:
        return lambda x: type_(x[key]) if key in x else None

    M = TypeVar("M", bound=ResponseModel)

    @staticmethod
    def get_as_model(
        key: str, model: Type[M], map_def: Optional[ResponseMappingDefinition] = None
    ) -> ExtractorDef[M]:
        if type(model) == str:
            model = Extractors.__import_class(model)
        return lambda x: map_to_class(x[key], model, map_def) if key in x else None

    @staticmethod
    def get_with(key: str, mapper: Callable[[S], T]) -> ExtractorDef[T]:
        return lambda x: mapper(x[key]) if key in x else None

    @staticmethod
    def get_list_with(key: str, mapper: Callable[[Any], T]) -> ExtractorDef[List[T]]:
        return lambda x: [mapper(i) for i in x[key]] if key in x else None

    @staticmethod
    def get_list_of_model(key: str, model: Type[M]) -> ExtractorDef[List[M]]:
        if type(model) == str:
            model = Extractors.__import_class(model)
        return lambda x: [map_to_class(i, model) for i in x[key]] if key in x else None

    @staticmethod
    def get_datetime(key: str) -> ExtractorDef[datetime]:
        return Extractors.get_with(key, lambda x: datetime.fromtimestamp(float(x)))

    @staticmethod
    def __import_class(model: str) -> Type[ResponseModel]:
        import importlib

        module_name, class_name = model.rsplit(".", 1)
        return getattr(importlib.import_module(module_name), class_name)


R = ResponseMappingDefinition

mapping_definitions: Dict[Type[ResponseModel], ResponseMappingDefinition] = {
    Item: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("status", "status", Extractors.get("status")),
            ResponseProperty("name", "name", Extractors.get("name")),
            ResponseProperty("price", "price", Extractors.get("price")),
        ],
        optional_properties=[
            ResponseProperty(
                "seller", "seller", Extractors.get_as_model("seller", Seller)
            ),
            ResponseProperty(
                "description", "description", Extractors.get("description")
            ),
            ResponseProperty("photos", "photos", Extractors.get("photos")),
            ResponseProperty(
                "photo_paths", "photo_paths", Extractors.get("photo_paths")
            ),
            ResponseProperty("thumbnails", "thumbnails", Extractors.get("thumbnails")),
            ResponseProperty(
                "item_category",
                "item_category",
                Extractors.get_as_model("item_category", ItemCategorySummary),
            ),
            ResponseProperty(
                "item_condition",
                "item_condition",
                Extractors.get_as_model("item_condition", ItemCondition),
            ),
            ResponseProperty(
                "colors",
                "colors",
                Extractors.get_list_of_model("colors", Color),
            ),
            ResponseProperty(
                "shipping_payer",
                "shipping_payer",
                Extractors.get_as_model("shipping_payer", ShippingPayer),
            ),
            ResponseProperty(
                "shipping_method",
                "shipping_method",
                Extractors.get_as_model("shipping_method", ShippingMethod),
            ),
            ResponseProperty(
                "shipping_from_area",
                "shipping_from_area",
                Extractors.get_as_model("shipping_from_area", ShippingFromArea),
            ),
            ResponseProperty(
                "shipping_duration",
                "shipping_duration",
                Extractors.get_as_model("shipping_duration", ShippingDuration),
            ),
            ResponseProperty(
                "shipping_class",
                "shipping_class",
                Extractors.get_as_model("shipping_class", ShippingClass),
            ),
            ResponseProperty("num_likes", "num_likes", Extractors.get("num_likes")),
            ResponseProperty(
                "num_comments", "num_comments", Extractors.get("num_comments")
            ),
            ResponseProperty(
                "comments",
                "comments",
                Extractors.get_list_of_model("comments", Comment),
            ),
            ResponseProperty("updated", "updated", Extractors.get_datetime("updated")),
            ResponseProperty("created", "created", Extractors.get_datetime("created")),
            ResponseProperty("pager_id", "pager_id", Extractors.get("pager_id")),
            ResponseProperty("liked", "liked", Extractors.get("liked")),
            ResponseProperty("checksum", "checksum", Extractors.get("checksum")),
            ResponseProperty(
                "is_dynamic_shipping_fee",
                "is_dynamic_shipping_fee",
                Extractors.get("is_dynamic_shipping_fee"),
            ),
            # unknown schema:
            ResponseProperty(
                "application_attributes",
                "application_attributes",
                Extractors.get("application_attributes"),
            ),
            ResponseProperty(
                "is_shop_item", "is_shop_item", Extractors.get("is_shop_item")
            ),
            ResponseProperty(
                "is_anonymous_shipping",
                "is_anonymous_shipping",
                Extractors.get("is_anonymous_shipping"),
            ),
            ResponseProperty(
                "is_web_visible", "is_web_visible", Extractors.get("is_web_visible")
            ),
            ResponseProperty(
                "is_offerable", "is_offerable", Extractors.get("is_offerable")
            ),
            ResponseProperty(
                "is_organizational_user",
                "is_organizational_user",
                Extractors.get("is_organizational_user"),
            ),
            ResponseProperty(
                "organizational_user_status",
                "organizational_user_status",
                Extractors.get("organizational_user_status"),
            ),
            ResponseProperty(
                "is_stock_item", "is_stock_item", Extractors.get("is_stock_item")
            ),
            ResponseProperty(
                "is_cancelable", "is_cancelable", Extractors.get("is_cancelable")
            ),
            ResponseProperty(
                "shipped_by_worker",
                "shipped_by_worker",
                Extractors.get("shipped_by_worker"),
            ),
            # unknown list, ignore: additional_services
            ResponseProperty(
                "has_additional_service",
                "has_additional_service",
                Extractors.get("has_additional_service"),
            ),
            ResponseProperty(
                "has_like_list", "has_like_list", Extractors.get("has_like_list")
            ),
            ResponseProperty(
                "is_offerable_v2", "is_offerable_v2", Extractors.get("is_offerable_v2")
            ),
        ],
    ),
    Seller: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
        ],
        optional_properties=[
            ResponseProperty("photo_url", "photo", Extractors.get("photo_url")),
            ResponseProperty(
                "photo_thumbnail_url",
                "photo_thumbnail",
                Extractors.get("photo_thumbnail_url"),
            ),
            ResponseProperty(
                "register_sms_confirmation",
                "register_sms_confirmation",
                Extractors.get("register_sms_confirmation"),
            ),
            ResponseProperty(
                "register_sms_confirmation_at",
                "register_sms_confirmation_at",
                Extractors.get_with(
                    "register_sms_confirmation_at",
                    lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"),
                ),
            ),
            ResponseProperty("created", "created", Extractors.get_datetime("created")),
            ResponseProperty(
                "num_sell_items", "num_sell_items", Extractors.get("num_sell_items")
            ),
            ResponseProperty(
                "ratings",
                "ratings",
                Extractors.get_as_model("ratings", Seller.Ratings),
            ),
            ResponseProperty(
                "num_ratings", "num_ratings", Extractors.get("num_ratings")
            ),
            ResponseProperty("score", "score", Extractors.get("score")),
            ResponseProperty(
                "is_official", "is_official", Extractors.get("is_official")
            ),
            ResponseProperty(
                "quick_shipper", "quick_shipper", Extractors.get("quick_shipper")
            ),
            ResponseProperty(
                "star_rating_score",
                "star_rating_score",
                Extractors.get("star_rating_score"),
            ),
        ],
    ),
    Seller.Ratings: R(
        required_properties=[
            ResponseProperty("good", "good", Extractors.get("good")),
            ResponseProperty("normal", "normal", Extractors.get("normal")),
            ResponseProperty("bad", "bad", Extractors.get("bad")),
        ],
        optional_properties=[],
    ),
    ItemCondition: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
        ],
        optional_properties=[],
    ),
    Color: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
            ResponseProperty(
                "rgb", "rgb", Extractors.get_with("rgb", lambda x: int(x[1:], 16))
            ),
        ],
        optional_properties=[],
    ),
    ShippingPayer: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
        ],
        optional_properties=[
            ResponseProperty("code", "code", Extractors.get("code")),
        ],
    ),
    ShippingMethod: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
        ],
        optional_properties=[
            ResponseProperty(
                "is_deprecated", "is_deprecated", Extractors.get("is_deprecated")
            ),
        ],
    ),
    ShippingFromArea: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
        ],
        optional_properties=[],
    ),
    ShippingDuration: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
            ResponseProperty("min_days", "min_days", Extractors.get("min_days")),
            ResponseProperty("max_days", "max_days", Extractors.get("max_days")),
        ],
        optional_properties=[],
    ),
    ShippingClass: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("fee", "fee", Extractors.get("fee")),
            ResponseProperty("icon_id", "icon_id", Extractors.get("icon_id")),
            ResponseProperty("pickup_fee", "pickup_fee", Extractors.get("pickup_fee")),
            ResponseProperty(
                "shipping_fee", "shipping_fee", Extractors.get("shipping_fee")
            ),
            ResponseProperty("total_fee", "total_fee", Extractors.get("total_fee")),
            ResponseProperty("is_pickup", "is_pickup", Extractors.get("is_pickup")),
        ],
        optional_properties=[],
    ),
    Comment: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("message", "message", Extractors.get("message")),
        ],
        optional_properties=[
            ResponseProperty(
                "user", "user", Extractors.get_as_model("user", Comment.User)
            ),
            ResponseProperty("created", "created", Extractors.get_datetime("created")),
        ],
    ),
    Comment.User: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
        ],
        optional_properties=[
            ResponseProperty("photo_url", "photo", Extractors.get("photo_url")),
            ResponseProperty(
                "photo_thumbnail_url",
                "photo_thumbnail",
                Extractors.get("photo_thumbnail_url"),
            ),
        ],
    ),
    Items: R(
        required_properties=[
            ResponseProperty(
                "data", "items", Extractors.get_list_of_model("data", SellerItem)
            ),
        ],
        optional_properties=[],
    ),
    SellerItem: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty(
                "seller",
                "seller_id",
                Extractors.get_with(
                    "seller", lambda x: str(x["id"]) if "id" in x else None
                ),
            ),
            ResponseProperty("status", "status", Extractors.get("status")),
            ResponseProperty("name", "name", Extractors.get("name")),
            ResponseProperty("price", "price", Extractors.get("price")),
        ],
        optional_properties=[
            ResponseProperty("thumbnails", "thumbnails", Extractors.get("thumbnails")),
            ResponseProperty(
                "root_category_id",
                "root_category_id",
                Extractors.get("root_category_id"),
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
                Extractors.get_as_model("item_category", ItemCategorySummary),
            ),
            ResponseProperty(
                "shipping_from_area",
                "shipping_from_area",
                Extractors.get_as_model("shipping_from_area", ShippingFromArea),
            ),
        ],
    ),
    Profile: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
        ],
        optional_properties=[
            ResponseProperty("photo_url", "photo_url", Extractors.get("photo_url")),
            ResponseProperty(
                "photo_thumbnail_url",
                "photo_thumbnail_url",
                Extractors.get("photo_thumbnail_url"),
            ),
            ResponseProperty(
                "register_sms_confirmation",
                "register_sms_confirmation",
                Extractors.get("register_sms_confirmation"),
            ),
            ResponseProperty(
                "ratings",
                "ratings",
                Extractors.get_as_model("ratings", Profile.Ratings),
            ),
            ResponseProperty(
                "polarized_ratings",
                "polarized_ratings",
                Extractors.get_as_model("polarized_ratings", Profile.PolarizedRatings),
            ),
            ResponseProperty(
                "num_ratings", "num_ratings", Extractors.get("num_ratings")
            ),
            ResponseProperty(
                "star_rating_score",
                "star_rating_score",
                Extractors.get("star_rating_score"),
            ),
            ResponseProperty(
                "is_followable", "is_followable", Extractors.get("is_followable")
            ),
            ResponseProperty("is_blocked", "is_blocked", Extractors.get("is_blocked")),
            ResponseProperty(
                "following_count", "following_count", Extractors.get("following_count")
            ),
            ResponseProperty(
                "follower_count", "follower_count", Extractors.get("follower_count")
            ),
            ResponseProperty("score", "score", Extractors.get("score")),
            ResponseProperty("created", "created", Extractors.get_datetime("created")),
            ResponseProperty("proper", "proper", Extractors.get("proper")),
            ResponseProperty(
                "introduction", "introduction", Extractors.get("introduction")
            ),
            ResponseProperty(
                "is_official", "is_official", Extractors.get("is_official")
            ),
            ResponseProperty(
                "num_sell_items", "num_sell_items", Extractors.get("num_sell_items")
            ),
            ResponseProperty("num_ticket", "num_ticket", Extractors.get("num_ticket")),
            ResponseProperty(
                "bounce_mail_flag",
                "bounce_mail_flag",
                Extractors.get("bounce_mail_flag"),
            ),
            # useless without authorization context
            # ('is_following', 'is_following', Extractors.get('is_following'))
            ResponseProperty(
                "current_point", "current_point", Extractors.get("current_point")
            ),
            ResponseProperty(
                "current_sales", "current_sales", Extractors.get("current_sales")
            ),
            ResponseProperty(
                "is_organizational_user",
                "is_organizational_user",
                Extractors.get("is_organizational_user"),
            ),
        ],
    ),
    Profile.PolarizedRatings: R(
        required_properties=[
            ResponseProperty("good", "good", Extractors.get("good")),
            ResponseProperty("bad", "bad", Extractors.get("bad")),
        ],
        optional_properties=[],
    ),
    Profile.Ratings: R(
        required_properties=[
            ResponseProperty("good", "good", Extractors.get("good")),
            ResponseProperty("normal", "normal", Extractors.get("normal")),
            ResponseProperty("bad", "bad", Extractors.get("bad")),
        ],
        optional_properties=[],
    ),
    SearchResults: R(
        required_properties=[
            ResponseProperty("meta", "meta", Extractors.get_as_model("meta", Meta)),
            ResponseProperty(
                "items",
                "items",
                Extractors.get_list_of_model("items", SearchResultItem),
            ),
        ],
        optional_properties=[],
    ),
    Meta: R(
        required_properties=[
            ResponseProperty(
                "nextPageToken", "next_page_token", Extractors.get("nextPageToken")
            ),
            ResponseProperty(
                "previousPageToken",
                "prev_page_token",
                Extractors.get("previousPageToken"),
            ),
            ResponseProperty(
                "numFound", "num_found", Extractors.get_as("numFound", int)
            ),
        ],
        optional_properties=[],
    ),
    SearchResultItem: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
            ResponseProperty("price", "price", Extractors.get_as("price", int)),
        ],
        optional_properties=[
            ResponseProperty("sellerId", "seller_id", Extractors.get("sellerId")),
            ResponseProperty("status", "status", Extractors.get("status")),
            ResponseProperty("created", "created", Extractors.get_datetime("created")),
            ResponseProperty("updated", "updated", Extractors.get_datetime("updated")),
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
            ResponseProperty(
                "shippingMethodId",
                "shipping_method_id",
                Extractors.get_as("shippingMethodId", int),
            ),
            ResponseProperty(
                "categoryId",
                "category_id",
                Extractors.get_as("categoryId", int),
            ),
            ResponseProperty("isNoPrice", "is_no_price", Extractors.get("isNoPrice")),
        ],
    ),
    ItemCategory: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
        ],
        optional_properties=[
            ResponseProperty(
                "display_order", "display_order", Extractors.get("display_order")
            ),
            ResponseProperty("tab_order", "tab_order", Extractors.get("tab_order")),
            ResponseProperty(
                "parent_category_id",
                "parent_category_id",
                Extractors.get("parent_category_id"),
            ),
            ResponseProperty(
                "parent_category_name",
                "parent_category_name",
                Extractors.get("parent_category_name"),
            ),
            ResponseProperty(
                "root_category_id",
                "root_category_id",
                Extractors.get("root_category_id"),
            ),
            ResponseProperty(
                "root_category_name",
                "root_category_name",
                Extractors.get("root_category_name"),
            ),
            ResponseProperty(
                "size_group_id", "size_group_id", Extractors.get("size_group_id")
            ),
            ResponseProperty(
                "brand_group_id", "brand_group_id", Extractors.get("brand_group_id")
            ),
            ResponseProperty(
                "children",
                "children",
                Extractors.get_list_of_model("children", ItemCategory),
            ),
        ],
    ),
    ItemCategorySummary: R(
        required_properties=[
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
        ],
        optional_properties=[
            ResponseProperty(
                "display_order", "display_order", Extractors.get("display_order")
            ),
            ResponseProperty(
                "parent_category_id",
                "parent_category_id",
                Extractors.get("parent_category_id"),
            ),
            ResponseProperty(
                "parent_category_name",
                "parent_category_name",
                Extractors.get("parent_category_name"),
            ),
            ResponseProperty(
                "root_category_id",
                "root_category_id",
                Extractors.get("root_category_id"),
            ),
            ResponseProperty(
                "root_category_name",
                "root_category_name",
                Extractors.get("root_category_name"),
            ),
        ],
    ),
}

RM = TypeVar("RM", bound=ResponseModel)


def map_to_class(
    response: dict,
    clazz: Type[RM],
    mapping_definition: ResponseMappingDefinition = None,
) -> RM:
    if clazz == ResponseModel:
        raise TypeError(
            "map_to_class() is supposed to be called with ResponseModel subclass as a parameter"
        )

    if mapping_definition is None:
        mapping_definition = mapping_definitions.get(clazz)
    if mapping_definition is None:
        raise ValueError(f"Mapping definition is not provided for {clazz.__name__}")

    init_properties = {}

    for prop in mapping_definition.required_properties:
        try:
            raw_prop = prop.extractor(response)
            if raw_prop is None:
                raise ValueError("Extractor returned None value")
            init_properties[prop.model_property_name] = raw_prop
        except Exception as exc:
            raise ParseAPIResponseError(
                f"Failed to retrieve required {clazz.__name__} property {prop.raw_property_name} from the response"
            ) from exc

    for prop in mapping_definition.optional_properties:
        raw_prop = None
        try:
            raw_prop = prop.extractor(response)
        except Exception as exc:
            _report_incorrect_optional(prop.raw_property_name, response, exc)
        init_properties[prop.model_property_name] = raw_prop

    return clazz(**init_properties)


def _report_incorrect_optional(prop: str, response: dict, exc: Exception) -> None:
    logging.warning(
        f"Encountered optional response property {prop} that could not be parsed correctly."
    )
    logging.debug(f"Response body: {response}\nError: {exc}")
