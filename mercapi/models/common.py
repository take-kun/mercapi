from dataclasses import dataclass
from typing import List

from mercapi.models.base import ResponseModel


@dataclass
class ItemCategory(ResponseModel):
    id_: int
    name: str
    tab_order: int
    display_order: int
    parent_category_id: int
    parent_category_name: str
    root_category_id: int
    root_category_name: str
    size_group_id: int
    brand_group_id: int
    children: List["ItemCategory"]


@dataclass
class ItemCategorySummary(ResponseModel):
    id_: int
    name: str
    display_order: int
    parent_category_id: int
    parent_category_name: str
    root_category_id: int
    root_category_name: str
