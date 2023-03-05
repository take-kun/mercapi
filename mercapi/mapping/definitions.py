import logging
from datetime import datetime
from typing import NamedTuple, List, Dict, TypeVar, Type, Any, Optional, Callable

from mercapi.models import Item
from mercapi.models.common import ItemCategory
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
        [
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("status", "status", Extractors.get("status")),
            ResponseProperty("name", "name", Extractors.get("name")),
            ResponseProperty("price", "price", Extractors.get("price")),
        ],
        [
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
                Extractors.get_as_model("item_category", ItemCategory),
            ),
            ResponseProperty(
                "item_condition",
                "item_condition",
                Extractors.get_as_model("item_condition", ItemCondition),
            ),
            ResponseProperty(
                "colors",
                "colors",
                Extractors.get_list_with("colors", lambda x: Color.from_dict(x)),
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
                Extractors.get_list_with("comments", lambda x: Comment.from_dict(x)),
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
    )
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