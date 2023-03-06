from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mercapi.models import Items
from mercapi.models.base import ResponseModel


@dataclass
class Profile(ResponseModel):
    @dataclass
    class Ratings(ResponseModel):
        good: int
        normal: int
        bad: int

    @dataclass
    class PolarizedRatings(ResponseModel):
        good: int
        bad: int

    id_: str
    name: str
    photo_url: str
    photo_thumbnail_url: str
    register_sms_confirmation: str
    ratings: Ratings
    polarized_ratings: PolarizedRatings
    num_ratings: int
    star_rating_score: int
    is_followable: bool
    is_blocked: bool
    following_count: int
    follower_count: int
    score: int
    created: datetime
    proper: bool
    introduction: str
    is_official: bool
    num_sell_items: int
    num_ticket: int
    bounce_mail_flag: str
    current_point: int
    current_sales: int
    is_organizational_user: bool

    async def items(self) -> "Items":
        return await self._mercapi.items(self.id_)
