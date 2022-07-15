import logging
from datetime import datetime
from typing import NamedTuple, Callable, List, TypeVar, Any, Type, Union

from mercapi.util.errors import ParseAPIResponseError


class ResponseProperty(NamedTuple):
    raw_property_name: str
    model_property_name: str
    extractor: Callable[[str], str]


class ResponseModel:

    _required_properties: List[ResponseProperty]
    _optional_properties: List[ResponseProperty]

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def from_dict(cls, d: dict):
        if cls == ResponseModel:
            raise TypeError('from_dict() class method is supposed to be called on ResponseModel subclasses providing '
                            'lists of properties')

        model_properties = {}

        for raw_name, model_name, func in cls._required_properties:
            try:
                raw_property = func(d)
                model_properties[model_name] = raw_property
            except Exception as e:
                raise ParseAPIResponseError(
                    f'Failed to retrieve required {cls.__name__} property {raw_name} from the response'
                ) from e

        for raw_name, model_name, func in cls._optional_properties:
            try:
                raw_property = func(d)
                model_properties[model_name] = raw_property
            except Exception as e:
                cls._report_incorrect_optional(raw_name, d, e)

        return cls(**model_properties)

    @classmethod
    def _report_incorrect_optional(cls, prop: str, response: dict, exc: Exception) -> None:
        logging.warning(
            f'Encountered optional response property {prop} that could not be parsed correctly.'
        )
        logging.debug(f'Response body: {response}\nError: {exc}')


class Extractors:
    """
    Collection of HOFs for parsing API responses in the most common ways.

    Each extractor function MUST handle lack of requested key
    in the response object (dict) and return None in such cases.
    """

    T = TypeVar('T')
    ExtractorDef = Callable[[dict], Union[T, None]]

    @staticmethod
    def get(key: str) -> ExtractorDef[Any]:
        return lambda x: x.get(key)

    S = TypeVar('S', int, float, str)

    @staticmethod
    def get_as(key: str, type_: Type[S]) -> ExtractorDef[S]:
        return lambda x: type_(x[key]) if key in x else None

    @staticmethod
    def get_with(key: str, mapper: Callable[[S], T]) -> ExtractorDef[T]:
        return lambda x: mapper(x[key]) if key in x else None

    @staticmethod
    def get_list_with(key: str, mapper: Callable[[Any], T]) -> ExtractorDef[List[T]]:
        return lambda x: [mapper(i) for i in x[key]] if key in x else None

    @staticmethod
    def get_datetime(key: str) -> ExtractorDef[datetime]:
        return Extractors.get_with(key, lambda x: datetime.utcfromtimestamp(float(x)))
