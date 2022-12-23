from datetime import datetime

from mercapi.models.base import Extractors, ResponseModel, ResponseProperty


class Seller(ResponseModel):
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

    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty("name", "name", Extractors.get("name")),
    ]
    _optional_properties = [
        ResponseProperty("photo_url", "photo", Extractors.get("photo_url")),
        ResponseProperty(
            "photo_thumbnail_url",
            "photo_thumbnail",
            Extractors.get("photo_thumbnail_url"),
        ),
        ResponseProperty(
            "register_sms_confirmation",
            "register_sms_confirmation",
            Extractors.get("register_sms_confirmation"),
        ),
        ResponseProperty(
            "register_sms_confirmation_at",
            "register_sms_confirmation_at",
            Extractors.get_with(
                "register_sms_confirmation_at",
                lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"),
            ),
        ),
        ResponseProperty("created", "created", Extractors.get_datetime("created")),
        ResponseProperty(
            "num_sell_items", "num_sell_items", Extractors.get("num_sell_items")
        ),
        ResponseProperty(
            "ratings",
            "ratings",
            Extractors.get_with("ratings", lambda x: Seller.Ratings.from_dict(x)),
        ),
        ResponseProperty("num_ratings", "num_ratings", Extractors.get("num_ratings")),
        ResponseProperty("score", "score", Extractors.get("score")),
        ResponseProperty("is_official", "is_official", Extractors.get("is_official")),
        ResponseProperty(
            "quick_shipper", "quick_shipper", Extractors.get("quick_shipper")
        ),
        ResponseProperty(
            "star_rating_score",
            "star_rating_score",
            Extractors.get("star_rating_score"),
        ),
    ]

    def __init__(
        self,
        id_: int,
        name: str,
        photo: str,
        photo_thumbnail: str,
        register_sms_confirmation: str,
        register_sms_confirmation_at: datetime,
        created: datetime,
        num_sell_items: int,
        ratings: Ratings,
        num_ratings: int,
        score: int,
        is_official: bool,
        quick_shipper: bool,
        star_rating_score: int,
    ):
        super().__init__()
        self.id_ = id_
        self.name = name
        self.photo = photo
        self.photo_thumbnail = photo_thumbnail
        self.register_sms_confirmation = register_sms_confirmation
        self.register_sms_confirmation_at = register_sms_confirmation_at
        self.created = created
        self.num_sell_items = num_sell_items
        self.ratings = ratings
        self.num_ratings = num_ratings
        self.score = score
        self.is_official = is_official
        self.quick_shipper = quick_shipper
        self.star_rating_score = star_rating_score


class ItemCondition(ResponseModel):
    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty("name", "name", Extractors.get("name")),
    ]
    _optional_properties = []

    def __init__(self, id_: int, name: str):
        super().__init__()
        self.id_ = id_
        self.name = name


class Color(ResponseModel):
    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty("name", "name", Extractors.get("name")),
        ResponseProperty(
            "rgb", "rgb", Extractors.get_with("rgb", lambda x: int(x[1:], 16))
        ),
    ]
    _optional_properties = []

    def __init__(self, id_: int, name: str, rgb: int):
        super().__init__()
        self.id_ = id_
        self.name = name
        self.rgb = rgb

    @property
    def rgb_code(self) -> str:
        return hex(self.rgb)


class ShippingPayer(ResponseModel):
    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty("name", "name", Extractors.get("name")),
    ]
    _optional_properties = [
        ResponseProperty("code", "code", Extractors.get("code")),
    ]

    def __init__(self, id_: int, name: str, code: str):
        super().__init__()
        self.id_ = id_
        self.name = name
        self.code = code


class ShippingMethod(ResponseModel):
    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty("name", "name", Extractors.get("name")),
    ]
    _optional_properties = [
        ResponseProperty(
            "is_deprecated", "is_deprecated", Extractors.get("is_deprecated")
        ),
    ]

    def __init__(self, id_: int, name: str, is_deprecated: str):
        super().__init__()
        self.id_ = id_
        self.name = name
        self.is_deprecated = is_deprecated


class ShippingFromArea(ResponseModel):
    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty("name", "name", Extractors.get("name")),
    ]
    _optional_properties = []

    def __init__(self, id_: int, name: str):
        super().__init__()
        self.id_ = id_
        self.name = name


class ShippingDuration(ResponseModel):
    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty("name", "name", Extractors.get("name")),
        ResponseProperty("min_days", "min_days", Extractors.get("min_days")),
        ResponseProperty("max_days", "max_days", Extractors.get("max_days")),
    ]
    _optional_properties = []

    def __init__(self, id_: int, name: str, min_days: int, max_days: int):
        super().__init__()
        self.id_ = id_
        self.name = name
        self.min_days = min_days
        self.max_days = max_days


class ShippingClass(ResponseModel):
    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty("fee", "fee", Extractors.get("fee")),
        ResponseProperty("icon_id", "icon_id", Extractors.get("icon_id")),
        ResponseProperty("pickup_fee", "pickup_fee", Extractors.get("pickup_fee")),
        ResponseProperty(
            "shipping_fee", "shipping_fee", Extractors.get("shipping_fee")
        ),
        ResponseProperty("total_fee", "total_fee", Extractors.get("total_fee")),
        ResponseProperty("is_pickup", "is_pickup", Extractors.get("is_pickup")),
    ]
    _optional_properties = []

    def __init__(
        self,
        id_: int,
        fee: int,
        icon_id: int,
        pickup_fee: int,
        shipping_fee: int,
        total_fee: int,
        is_pickup: bool,
    ):
        super().__init__()
        self.id_ = id_
        self.fee = fee
        self.icon_id = icon_id
        self.pickup_fee = pickup_fee
        self.shipping_fee = shipping_fee
        self.total_fee = total_fee
        self.is_pickup = is_pickup


class Comment(ResponseModel):
    class User(ResponseModel):
        _required_properties = [
            ResponseProperty("id", "id_", Extractors.get("id")),
            ResponseProperty("name", "name", Extractors.get("name")),
        ]
        _optional_properties = [
            ResponseProperty("photo_url", "photo", Extractors.get("photo_url")),
            ResponseProperty(
                "photo_thumbnail_url",
                "photo_thumbnail",
                Extractors.get("photo_thumbnail_url"),
            ),
        ]

        def __init__(self, id_: int, name: str, photo: str, photo_thumbnail: str):
            super().__init__()
            self.id_ = id_
            self.name = name
            self.photo = photo
            self.photo_thumbnail = photo_thumbnail

    _required_properties = [
        ResponseProperty("id", "id_", Extractors.get("id")),
        ResponseProperty("message", "message", Extractors.get("message")),
    ]
    _optional_properties = [
        ResponseProperty("user", "user", Extractors.get_as_model("user", User)),
        ResponseProperty("created", "created", Extractors.get_datetime("created")),
    ]
