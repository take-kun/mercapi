from typing import List, TypeVar

from mercapi.models import ResponseModel
from mercapi.models.base import Extractors


IC = TypeVar('IC', bound='ItemCategory')


class ItemCategory(ResponseModel):
    _required_properties = [
        ('id', 'id_', Extractors.get('id')),
        ('name', 'name', Extractors.get('name')),
    ]
    _optional_properties = [
        ('display_order', 'display_order', Extractors.get('display_order')),
        ('parent_category_id', 'parent_category_id', Extractors.get('parent_category_id')),
        ('parent_category_name', 'parent_category_name', Extractors.get('parent_category_name')),
        ('root_category_id', 'root_category_id', Extractors.get('root_category_id')),
        ('root_category_name', 'root_category_name', Extractors.get('root_category_name')),
    ]

    def __init__(self, id_: int, name: str, display_order: int, parent_category_id: int,
                 parent_category_name: str, root_category_id: int,
                 root_category_name: str, children: List['ItemCategory']):
        super().__init__()
        self.id_ = id_
        self.name = name
        self.display_order = display_order
        self.parent_category_id = parent_category_id
        self.parent_category_name = parent_category_name
        self.root_category_id = root_category_id
        self.root_category_name = root_category_name
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
        if not any(raw_name == 'child' for raw_name, _, _ in cls._optional_properties):
            cls._optional_properties.append(('child', 'children', Extractors.get_list_of_model('child', cls)))
        return super().from_dict(d)

    @property
    def parent_category(self):
        if self.parent_category_id is not None and self.parent_category_name is not None:
            return ItemCategory(**{'id_': self.parent_category_id, 'name': self.parent_category_name})
        else:
            return None

    @property
    def root_category(self):
        if self.root_category_id is not None and self.root_category_name is not None:
            return ItemCategory(**{'id_': self.root_category_id, 'name': self.root_category_name})
        else:
            return None
