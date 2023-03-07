from datetime import datetime
from typing import (
    NamedTuple,
    Callable,
    List,
    TypeVar,
    Any,
    Type,
    TYPE_CHECKING,
    Optional,
)

if TYPE_CHECKING:
    from mercapi import Mercapi

RM = TypeVar("RM", bound="ResponseModel")
T = TypeVar("T")
ExtractorDef = Callable[[dict], Optional[T]]


class ResponseProperty(NamedTuple):
    raw_property_name: str
    model_property_name: str
    extractor: ExtractorDef


class ResponseModel:

    _mercapi: "Mercapi"

    @classmethod
    def set_mercapi(cls, mercapi: "Mercapi") -> None:
        cls._mercapi = mercapi


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
    def get_as_model(key: str, model: Type[M]) -> ExtractorDef[M]:
        if type(model) == str:
            model = Extractors.__import_class(model)
        return lambda x: model.from_dict(x[key]) if key in x else None

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
        return lambda x: [model.from_dict(i) for i in x[key]] if key in x else None

    @staticmethod
    def get_datetime(key: str) -> ExtractorDef[datetime]:
        return Extractors.get_with(key, lambda x: datetime.fromtimestamp(float(x)))

    @staticmethod
    def __import_class(model: str) -> Type[ResponseModel]:
        import importlib

        module_name, class_name = model.rsplit(".", 1)
        return getattr(importlib.import_module(module_name), class_name)
