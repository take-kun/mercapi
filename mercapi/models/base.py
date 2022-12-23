import logging
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
from mercapi.util.errors import ParseAPIResponseError


RM = TypeVar("RM", bound="ResponseModel")
T = TypeVar("T")
ExtractorDef = Callable[[dict], Optional[T]]


class ResponseProperty(NamedTuple):
    raw_property_name: str
    model_property_name: str
    extractor: ExtractorDef


class ResponseModel:

    _mercapi: "Mercapi"

    _required_properties: List[ResponseProperty]
    _optional_properties: List[ResponseProperty]

    def __init__(self, *args, **kwargs):
        pass

    def keys(self):
        return [
            p.model_property_name
            for p in self._required_properties + self._optional_properties
        ]

    def __getitem__(self, key):
        if key not in self.keys():
            raise IndexError(
                f"{key} is not a valid member of {self.__class__.__name__}"
            )
        return getattr(self, key)

    @classmethod
    def from_dict(cls, d: dict) -> RM:
        if cls == ResponseModel:
            raise TypeError(
                "from_dict() class method is supposed to be called on ResponseModel subclasses providing "
                "lists of properties"
            )

        model_properties = {}

        for prop in cls._required_properties:
            try:
                raw_property = prop.extractor(d)
                model_properties[prop.model_property_name] = raw_property
            except Exception as e:
                raise ParseAPIResponseError(
                    f"Failed to retrieve required {cls.__name__} property {prop.raw_property_name} from the response"
                ) from e

        for prop in cls._optional_properties:
            raw_property = None
            try:
                raw_property = prop.extractor(d)
            except Exception as e:
                cls._report_incorrect_optional(prop.raw_property_name, d, e)
            model_properties[prop.model_property_name] = raw_property

        return cls(**model_properties)

    @classmethod
    def set_mercapi(cls, m: "Mercapi") -> None:
        cls._mercapi = m

    @classmethod
    def _report_incorrect_optional(
        cls, prop: str, response: dict, exc: Exception
    ) -> None:
        logging.warning(
            f"Encountered optional response property {prop} that could not be parsed correctly."
        )
        logging.debug(f"Response body: {response}\nError: {exc}")


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
