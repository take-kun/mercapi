import pytest

from tests.models import ModelTest, ModelTestB, ModelTestBNested, ModelTestC, ModelTestD


def test_retrieve_existing_required_field():
    field_1 = "foo"
    obj = ModelTest(field_1, None)

    assert obj["field_1"] == field_1


def test_retrieve_existing_optional_field():
    field_1 = "foo"
    field_2 = "bar"
    obj = ModelTest(field_1, field_2)

    assert obj["field_2"] == field_2


def test_retrieve_existing_empty_optional_field():
    obj = ModelTest("foo", None)

    assert obj["field_2"] is None


def test_retrieve_non_existent_field_throw_exception():
    obj = ModelTest("foo", None)

    with pytest.raises(IndexError):
        obj["field_x"]


def test_convert_class_to_dict():
    obj = ModelTest("foo", "bar")
    dict_obj = dict(obj)

    assert dict_obj == {
        "field_1": obj.field_1,
        "field_2": obj.field_2,
    }


def test_unpack_class_as_kwargs():
    obj = ModelTest("foo", "bar")
    kwargs = dict(**obj)

    assert kwargs == {
        "field_1": obj.field_1,
        "field_2": obj.field_2,
    }


def test_convert_nested_class_to_dict():
    obj_nested = ModelTestBNested("foo", "bar")
    obj = ModelTestB("foo", obj_nested)
    dict_obj = dict(obj)

    assert dict_obj == {
        "field_1": obj.field_1,
        "field_nested": {
            "field_a": obj_nested.field_a,
            "field_b": obj_nested.field_b,
        },
    }


def test_convert_nested_list_to_dict():
    list_nested = [
        ModelTestBNested("foo0", "bar0"),
        ModelTestBNested("foo1", "bar1"),
        ModelTestBNested("foo2", "bar2"),
    ]
    obj = ModelTestC("foo", list_nested)
    dict_obj = dict(obj)

    assert dict_obj == {
        "field_1": obj.field_1,
        "list_nested": [
            {
                "field_a": "foo0",
                "field_b": "bar0",
            },
            {
                "field_a": "foo1",
                "field_b": "bar1",
            },
            {
                "field_a": "foo2",
                "field_b": "bar2",
            },
        ],
    }


def test_convert_nested_primitives_list_do_dict():
    list_nested = [0, 1, 2, 3, 9]
    obj = ModelTestD(list_nested)
    dict_obj = dict(obj)

    assert dict_obj == {
        "list_a": list_nested,
    }
