from dataclasses import dataclass
from typing import Optional, Dict, Type, List, Any

import pytest

import mercapi.mapping.definitions
from mercapi.mapping.definitions import (
    ResponseMappingDefinition,
    ResponseProperty,
    map_to_class,
    Extractors,
)
from mercapi.models.base import ResponseModel
from mercapi.util.errors import ParseAPIResponseError


@dataclass
class ModelTest(ResponseModel):
    field_1: str
    field_2: Optional[str]


@dataclass
class ModelTestBNested(ResponseModel):
    field_a: str
    field_b: Optional[str]


@dataclass
class ModelTestB(ResponseModel):
    field_1: str
    field_nested: ModelTestBNested


@dataclass
class ModelTestC(ResponseModel):
    list_a: List[Any]


@dataclass
class ModelTestD(ResponseModel):
    list_nested: List[ModelTest]


mapping_definitions: Dict[Type[ResponseModel], ResponseMappingDefinition] = {
    ModelTest: ResponseMappingDefinition(
        [ResponseProperty("field1", "field_1", Extractors.get("field1"))],
        [ResponseProperty("field2", "field_2", Extractors.get("field2"))],
    ),
    ModelTestB: ResponseMappingDefinition(
        [
            ResponseProperty("field1", "field_1", Extractors.get("field1")),
            ResponseProperty(
                "fieldNested",
                "field_nested",
                Extractors.get_as_model("fieldNested", ModelTestBNested),
            ),
        ],
        [],
    ),
    ModelTestBNested: ResponseMappingDefinition(
        [ResponseProperty("fieldA", "field_a", Extractors.get("fieldA"))],
        [ResponseProperty("fieldB", "field_b", Extractors.get("fieldB"))],
    ),
    ModelTestC: ResponseMappingDefinition(
        [
            ResponseProperty("listA", "list_a", Extractors.get("listA")),
        ],
        [],
    ),
    ModelTestD: ResponseMappingDefinition(
        [
            ResponseProperty(
                "listNested",
                "list_nested",
                Extractors.get_list_of_model("listNested", ModelTest),
            ),
        ],
        [],
    ),
}


def test_mapping_full_object():
    r = {
        "field1": "foo",
        "field2": "bar",
    }
    model = map_to_class(r, ModelTest, mapping_definitions[ModelTest])

    assert model.field_1 == "foo"
    assert model.field_2 == "bar"


def test_mapping_object_without_optionals():
    r = {
        "field1": "foo",
    }
    model = map_to_class(r, ModelTest, mapping_definitions[ModelTest])

    assert model.field_1 == "foo"
    assert model.field_2 is None


def test_mapping_object_without_required_props():
    r = {
        "field2": "bar",
    }
    with pytest.raises(ParseAPIResponseError):
        map_to_class(r, ModelTest, mapping_definitions[ModelTest])


def test_mapping_nested_object(monkeypatch):
    r = {
        "field1": "foo",
        "fieldNested": {
            "fieldA": "bar",
            "fieldB": "baz",
        },
    }
    monkeypatch.setitem(
        mercapi.mapping.definitions.mapping_definitions,
        ModelTestB,
        mapping_definitions[ModelTestB],
    )
    monkeypatch.setitem(
        mercapi.mapping.definitions.mapping_definitions,
        ModelTestBNested,
        mapping_definitions[ModelTestBNested],
    )
    model = map_to_class(r, ModelTestB)
    assert model.field_1 == "foo"
    assert model.field_nested == ModelTestBNested(field_a="bar", field_b="baz")


def test_mapping_list_of_primitives():
    r = {"listA": [0, 1, 2, 3, 4]}
    model = map_to_class(r, ModelTestC, mapping_definitions[ModelTestC])
    assert model.list_a == [0, 1, 2, 3, 4]


def test_mapping_list_of_nested_objects(monkeypatch):
    r = {
        "listNested": [
            {
                "field1": "foo",
                "field2": "bar",
            }
        ]
    }
    monkeypatch.setitem(
        mercapi.mapping.definitions.mapping_definitions,
        ModelTest,
        mapping_definitions[ModelTest],
    )
    monkeypatch.setitem(
        mercapi.mapping.definitions.mapping_definitions,
        ModelTestD,
        mapping_definitions[ModelTestD],
    )
    model = map_to_class(r, ModelTestD)
    assert len(model.list_nested) == 1
    assert model.list_nested[0] == ModelTest(field_1="foo", field_2="bar")
