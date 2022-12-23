from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mercapi.models import Items
from mercapi.models.base import Extractors, ResponseModel, ResponseProperty


class Profile(ResponseModel):
    class Ratings(ResponseModel):
        _required_properties = [
            ResponseProperty("good", "good", Extractors.get("good")),
            ResponseProperty("normal", "normal", Extractors.get("normal")),
            ResponseProperty("bad", "bad", Extractors.get("bad")),
        ]
        _optional_properties = []

        def __init__(self, good: int, normal: int, bad: int):
            super().__init__()
            self.good = good
            self.normal = normal
            self.bad = bad

    class PolarizedRatings(ResponseModel):
        _required_properties = [
            ResponseProperty("good", "good", Extractors.get("good")),
            ResponseProperty("bad", "bad", Extractors.get("bad")),
        ]
        _optional_properties = []

        def __init__(self, good: int, bad: int):
            super().__init__()
            self.good = good
            self.bad = bad

    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty("name", "name", Extractors.get("name")),
    ]

    _optional_properties = [
        ResponseProperty("photo_url", "photo_url", Extractors.get("photo_url")),
        ResponseProperty(
            "photo_thumbnail_url",
            "photo_thumbnail_url",
            Extractors.get("photo_thumbnail_url"),
        ),
        ResponseProperty(
            "register_sms_confirmation",
            "register_sms_confirmation",
            Extractors.get("register_sms_confirmation"),
        ),
        ResponseProperty(
            "ratings",
            "ratings",
            Extractors.get_with("ratings", lambda x: Profile.Ratings.from_dict(x)),
        ),
        ResponseProperty(
            "polarized_ratings",
            "polarized_ratings",
            Extractors.get_with(
                "polarized_ratings", lambda x: Profile.PolarizedRatings.from_dict(x)
            ),
        ),
        ResponseProperty("num_ratings", "num_ratings", Extractors.get("num_ratings")),
        ResponseProperty(
            "star_rating_score",
            "star_rating_score",
            Extractors.get("star_rating_score"),
        ),
        ResponseProperty(
            "is_followable", "is_followable", Extractors.get("is_followable")
        ),
        ResponseProperty("is_blocked", "is_blocked", Extractors.get("is_blocked")),
        ResponseProperty(
            "following_count", "following_count", Extractors.get("following_count")
        ),
        ResponseProperty(
            "follower_count", "follower_count", Extractors.get("follower_count")
        ),
        ResponseProperty("score", "score", Extractors.get("score")),
        ResponseProperty("created", "created", Extractors.get_datetime("created")),
        ResponseProperty("proper", "proper", Extractors.get("proper")),
        ResponseProperty(
            "introduction", "introduction", Extractors.get("introduction")
        ),
        ResponseProperty("is_official", "is_official", Extractors.get("is_official")),
        ResponseProperty(
            "num_sell_items", "num_sell_items", Extractors.get("num_sell_items")
        ),
        ResponseProperty("num_ticket", "num_ticket", Extractors.get("num_ticket")),
        ResponseProperty(
            "bounce_mail_flag", "bounce_mail_flag", Extractors.get("bounce_mail_flag")
        ),
        # useless without authorization context
        # ('is_following', 'is_following', Extractors.get('is_following'))
        ResponseProperty(
            "current_point", "current_point", Extractors.get("current_point")
        ),
        ResponseProperty(
            "current_sales", "current_sales", Extractors.get("current_sales")
        ),
        ResponseProperty(
            "is_organizational_user",
            "is_organizational_user",
            Extractors.get("is_organizational_user"),
        ),
    ]

    def __init__(
        self,
        id_: str,
        name: str,
        photo_url: str,
        photo_thumbnail_url: str,
        register_sms_confirmation: str,
        ratings: Ratings,
        polarized_ratings: PolarizedRatings,
        num_ratings: int,
        star_rating_score: int,
        is_followable: bool,
        is_blocked: bool,
        following_count: int,
        follower_count: int,
        score: int,
        created: datetime,
        proper: bool,
        introduction: str,
        is_official: bool,
        num_sell_items: int,
        num_ticket: int,
        bounce_mail_flag: str,
        current_point: int,
        current_sales: int,
        is_organizational_user: bool,
    ):
        super().__init__()
        self.id_ = id_
        self.name = name
        self.photo_url = photo_url
        self.photo_thumbnail_url = photo_thumbnail_url
        self.register_sms_confirmation = register_sms_confirmation
        self.ratings = ratings
        self.polarized_ratings = polarized_ratings
        self.num_ratings = num_ratings
        self.star_rating_score = star_rating_score
        self.is_followable = is_followable
        self.is_blocked = is_blocked
        self.following_count = following_count
        self.follower_count = follower_count
        self.score = score
        self.created = created
        self.proper = proper
        self.introduction = introduction
        self.is_official = is_official
        self.num_sell_items = num_sell_items
        self.num_ticket = num_ticket
        self.bounce_mail_flag = bounce_mail_flag
        self.current_point = current_point
        self.current_sales = current_sales
        self.is_organizational_user = is_organizational_user

    async def items(self) -> "Items":
        return await self._mercapi.items(self.id_)
