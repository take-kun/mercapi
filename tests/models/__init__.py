from typing import Optional, List

from mercapi.models.base import ResponseModel, Extractors, ResponseProperty


class ModelTest(ResponseModel):
    _required_properties = [
        ResponseProperty("field_1", "field_1", Extractors.get("field_1")),
    ]
    _optional_properties = [
        ResponseProperty("field_2", "field_2", Extractors.get("field_2")),
    ]

    def __init__(self, field_1: str, field_2: Optional[str]):
        super().__init__()
        self.field_1 = field_1
        self.field_2 = field_2


class ModelTestBNested(ResponseModel):
    _required_properties = [
        ResponseProperty("field_a", "field_a", Extractors.get("field_a")),
    ]
    _optional_properties = [
        ResponseProperty("field_b", "field_b", Extractors.get("field_b")),
    ]

    def __init__(self, field_a: str, field_b: Optional[str]):
        super().__init__()
        self.field_a = field_a
        self.field_b = field_b


class ModelTestB(ResponseModel):
    _required_properties = [
        ResponseProperty("field_1", "field_1", Extractors.get("field_1")),
        ResponseProperty(
            "field_nested",
            "field_nested",
            Extractors.get_as_model("field_nested", ModelTestBNested),
        ),
    ]
    _optional_properties = []

    def __init__(self, field_1: str, field_nested: ModelTestBNested):
        super().__init__()
        self.field_1 = field_1
        self.field_nested = field_nested


class ModelTestC(ResponseModel):
    _required_properties = [
        ResponseProperty("field_1", "field_1", Extractors.get("field_1")),
        ResponseProperty(
            "list_nested",
            "list_nested",
            Extractors.get_list_of_model("list_nested", ModelTestBNested),
        ),
    ]
    _optional_properties = []

    def __init__(self, field_1: str, list_nested: List[ModelTestBNested]):
        super().__init__()
        self.field_1 = field_1
        self.list_nested = list_nested


class ModelTestD(ResponseModel):
    _required_properties = [
        ResponseProperty("list_a", "list_a", Extractors.get("list_a")),
    ]
    _optional_properties = []

    def __init__(self, list_a: List[int]):
        super().__init__()
        self.list_a = list_a
