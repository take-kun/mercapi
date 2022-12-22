from typing import Optional

from mercapi.models.base import ResponseModel, Extractors, ResponseProperty


class TestModel(ResponseModel):
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
