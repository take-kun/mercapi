from typing import List, TypeVar

from mercapi.models.base import Extractors, ResponseModel, ResponseProperty

IC = TypeVar("IC", bound="ItemCategory")


class ItemCategory(ResponseModel):
    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty("name", "name", Extractors.get("name")),
    ]
    _optional_properties = [
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
            "root_category_id", "root_category_id", Extractors.get("root_category_id")
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
    ]

    def __init__(
        self,
        id_: int,
        name: str,
        tab_order: int,
        display_order: int,
        parent_category_id: int,
        parent_category_name: str,
        root_category_id: int,
        root_category_name: str,
        size_group_id: int,
        brand_group_id: int,
        children: List["ItemCategory"],
    ):
        super().__init__()
        self.id_ = id_
        self.name = name
        self.tab_order = tab_order
        self.display_order = display_order
        self.parent_category_id = parent_category_id
        self.parent_category_name = parent_category_name
        self.root_category_id = root_category_id
        self.root_category_name = root_category_name
        self.size_group_id = size_group_id
        self.brand_group_id = brand_group_id
        self.children = children

    @classmethod
    def from_dict(cls, d: dict) -> IC:
        # Dirty workaround for recursively parsing 'child' property which is a list
        # of ItemCategory objects. As a class cannot be self-referenced inside default properties,
        # like _required_properties and _optional_properties lists, this element is appended here
        # making use of 'cls' parameter.
        #
        # Alternative way of passing type to Extractors.get_list_of_model using module and class name
        # is not possible here due to cyclic imports hierarchy.
        if not any(raw_name == "child" for raw_name, _, _ in cls._optional_properties):
            cls._optional_properties.append(
                ResponseProperty(
                    "child", "children", Extractors.get_list_of_model("child", cls)
                )
            )
        return super().from_dict(d)
