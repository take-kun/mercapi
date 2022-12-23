import pytest

from tests.models import ModelTest


def test_retrieve_existing_required_field():
    field_1 = "foo"
    obj = ModelTest(field_1, None)

    assert obj["field_1"] == field_1


def test_retrieve_existing_optional_field():
    field_1 = "foo"
    field_2 = "bar"
    obj = ModelTest(field_1, field_2)

    assert obj["field_2"] == field_2


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
