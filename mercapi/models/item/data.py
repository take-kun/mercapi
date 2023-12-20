from dataclasses import dataclass
from datetime import datetime

from mercapi.models.base import ResponseModel


@dataclass
class Seller(ResponseModel):
    @dataclass
    class Ratings(ResponseModel):
        good: int
        normal: int
        bad: int

    id_: int
    name: str
    photo: str
    photo_thumbnail: str
    register_sms_confirmation: str
    register_sms_confirmation_at: datetime
    created: datetime
    num_sell_items: int
    ratings: Ratings
    num_ratings: int
    score: int
    is_official: bool
    quick_shipper: bool
    star_rating_score: int


@dataclass
class ItemCondition(ResponseModel):
    id_: int
    name: str


@dataclass
class Color(ResponseModel):
    id_: int
    name: str
    rgb: int

    @property
    def rgb_code(self) -> str:
        return hex(self.rgb)


@dataclass
class ShippingPayer(ResponseModel):
    id_: int
    name: str
    code: str


@dataclass
class ShippingMethod(ResponseModel):
    id_: int
    name: str
    is_deprecated: str


@dataclass
class ShippingFromArea(ResponseModel):
    id_: int
    name: str


@dataclass
class ShippingDuration(ResponseModel):
    id_: int
    name: str
    min_days: int
    max_days: int


@dataclass
class ShippingClass(ResponseModel):
    id_: int
    fee: int
    icon_id: int
    pickup_fee: int
    shipping_fee: int
    total_fee: int
    is_pickup: bool


@dataclass
class Comment(ResponseModel):
    @dataclass
    class User(ResponseModel):
        id_: int
        name: str
        photo: str
        photo_thumbnail: str

    id_: int
    message: str
    user: User
    created: datetime
