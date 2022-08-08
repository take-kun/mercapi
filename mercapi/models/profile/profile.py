from mercapi.models import ResponseModel
from mercapi.models.base import Extractors


class Profile(ResponseModel):
    class Ratings(ResponseModel):
        _required_properties = [
            ('good', 'good', Extractors.get('good')),
            ('normal', 'normal', Extractors.get('normal')),
            ('bad', 'bad', Extractors.get('bad')),
        ]
        _optional_properties = []

        def __init__(self, good: int, normal: int, bad: int):
            super().__init__()
            self.good = good
            self.normal = normal
            self.bad = bad

    class PolarizedRatings(ResponseModel):
        _required_properties = [
            ('good', 'good', Extractors.get('good')),
            ('bad', 'bad', Extractors.get('bad')),
        ]
        _optional_properties = []

        def __init__(self, good: int, bad: int):
            super().__init__()
            self.good = good
            self.bad = bad

    _required_properties = [
        ('id', 'id_', Extractors.get('id')),
        ('name', 'name', Extractors.get('name')),
    ]

    _optional_properties = [
        ('photo_url', 'photo_url', Extractors.get('photo_url')),
        ('photo_thumbnail_url', 'photo_thumbnail_url', Extractors.get('photo_thumbnail_url')),
        ('register_sms_confirmation', 'register_sms_confirmation', Extractors.get('register_sms_confirmation')),
        ('ratings', 'ratings', Extractors.get_with('ratings', lambda x: Profile.Ratings.from_dict(x))),
        ('polarized_ratings', 'polarized_ratings',
         Extractors.get_with('polarized_ratings', lambda x: Profile.PolarizedRatings.from_dict(x))),
        ('num_ratings', 'num_ratings', Extractors.get('num_ratings')),
        ('star_rating_score', 'star_rating_score', Extractors.get('star_rating_score')),
        ('is_followable', 'is_followable', Extractors.get('is_followable')),
        ('is_blocked', 'is_blocked', Extractors.get('is_blocked')),
        ('following_count', 'following_count', Extractors.get('following_count')),
        ('score', 'score', Extractors.get('score')),
        ('created', 'created', Extractors.get_datetime('created')),
        ('proper', 'proper', Extractors.get('proper')),
        ('introduction', 'introduction', Extractors.get('introduction')),
        ('is_official', 'is_official', Extractors.get('is_official')),
        ('num_sell_items', 'num_sell_items', Extractors.get('num_sell_items')),
        ('num_ticket', 'num_ticket', Extractors.get('num_ticket')),
        ('bounce_mail_flag', 'bounce_mail_flag', Extractors.get('bounce_mail_flag')),
        # useless without authorization context
        # ('is_following', 'is_following', Extractors.get('is_following'))
        ('current_point', 'current_point', Extractors.get('current_point')),
        ('current_sales', 'current_sales', Extractors.get('current_sales')),
        ('is_organizational_user', 'is_organizational_user', Extractors.get('is_organizational_user')),
    ]