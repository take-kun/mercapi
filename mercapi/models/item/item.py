from mercapi.models.item.data import *


# actually a mapping for 'data' object in item response
#
# consider nesting all the properties in data submodel
# if the original response gets more verbose
class Item(ResponseModel):
    _required_properties = [
        ('id', 'id_', Extractors.get('id')),
        ('status', 'status', Extractors.get('status')),
        ('name', 'name', Extractors.get('name')),
        ('price', 'price', Extractors.get('price')),
    ]
    _optional_properties = [
        ('seller', 'seller', Extractors.get_as_model('seller', Seller)),
        ('description', 'description', Extractors.get('description')),
        ('photos', 'photos', Extractors.get('photos')),
        ('photo_paths', 'photo_paths', Extractors.get('photo_paths')),
        ('thumbnails', 'thumbnails', Extractors.get('thumbnails')),
        ('item_category', 'item_category', Extractors.get_as_model('item_category', ItemCategory)),
        ('item_condition', 'item_condition', Extractors.get_as_model('item_condition', ItemCondition)),
        ('colors', 'colors', Extractors.get_list_with('colors', lambda x: Color.from_dict(x))),
        ('shipping_payer', 'shipping_payer', Extractors.get_as_model('shipping_payer', ShippingPayer)),
        ('shipping_method', 'shipping_method', Extractors.get_as_model('shipping_method', ShippingMethod)),
        ('shipping_from_area', 'shipping_from_area', Extractors.get_as_model('shipping_from_area', ShippingFromArea)),
        ('shipping_duration', 'shipping_duration', Extractors.get_as_model('shipping_duration', ShippingDuration)),
        ('shipping_class', 'shipping_class', Extractors.get_as_model('shipping_class', ShippingClass)),
        ('num_likes', 'num_likes', Extractors.get('num_likes')),
        ('num_comments', 'num_comments', Extractors.get('num_comments')),
        ('comments', 'comments', Extractors.get_list_with('comments', lambda x: Comment.from_dict(x))),
        ('updated', 'updated', Extractors.get_datetime('updated')),
        ('created', 'created', Extractors.get_datetime('created')),
        ('pager_id', 'pager_id', Extractors.get('pager_id')),
        ('liked', 'liked', Extractors.get('liked')),
        ('checksum', 'checksum', Extractors.get('checksum')),
        ('is_dynamic_shipping_fee', 'is_dynamic_shipping_fee', Extractors.get('is_dynamic_shipping_fee')),
        # unknown schema:
        ('application_attributes', 'application_attributes', Extractors.get('application_attributes')),
        ('is_shop_item', 'is_shop_item', Extractors.get('is_shop_item')),
        ('is_anonymous_shipping', 'is_anonymous_shipping', Extractors.get('is_anonymous_shipping')),
        ('is_web_visible', 'is_web_visible', Extractors.get('is_web_visible')),
        ('is_offerable', 'is_offerable', Extractors.get('is_offerable')),
        ('is_organizational_user', 'is_organizational_user', Extractors.get('is_organizational_user')),
        ('organizational_user_status', 'organizational_user_status', Extractors.get('organizational_user_status')),
        ('is_stock_item', 'is_stock_item', Extractors.get('is_stock_item')),
        ('is_cancelable', 'is_cancelable', Extractors.get('is_cancelable')),
        ('shipped_by_worker', 'shipped_by_worker', Extractors.get('shipped_by_worker')),
        # unknown list, ignore: additional_services
        ('has_additional_service', 'has_additional_service', Extractors.get('has_additional_service')),
        ('has_like_list', 'has_like_list', Extractors.get('has_like_list')),
        ('is_offerable_v2', 'is_offerable_v2', Extractors.get('is_offerable_v2')),
    ]

    def __init__(self, id_: str, seller: Seller, status: str, name: str, price: int, description: str,
                 photos: List[str], photo_paths: List[str], thumbnails: List[str], item_category: ItemCategory,
                 item_condition: ItemCondition, colors: List[Color], shipping_payer: ShippingPayer,
                 shipping_method: ShippingMethod, shipping_from_area: ShippingFromArea,
                 shipping_duration: ShippingDuration, shipping_class: ShippingClass, num_likes: int, num_comments: int,
                 comments: List[Comment], updated: datetime, created: datetime, pager_id: int, liked: bool,
                 checksum: str, is_dynamic_shipping_fee: bool, application_attributes: dict, is_shop_item: str,
                 is_anonymous_shipping: bool, is_web_visible: bool, is_offerable: bool, is_organizational_user: bool,
                 organizational_user_status: str, is_stock_item: bool, is_cancelable: bool, shipped_by_worker: bool,
                 has_additional_service: bool, has_like_list: bool, is_offerable_v2: bool):
        super().__init__()
        self.id_ = id_
        self.seller = seller
        self.status = status
        self.name = name
        self.price = price
        self.description = description
        self.photos = photos
        self.photo_paths = photo_paths
        self.thumbnails = thumbnails
        self.item_category = item_category
        self.item_condition = item_condition
        self.colors = colors
        self.shipping_payer = shipping_payer
        self.shipping_method = shipping_method
        self.shipping_from_area = shipping_from_area
        self.shipping_duration = shipping_duration
        self.shipping_class = shipping_class
        self.num_likes = num_likes
        self.num_comments = num_comments
        self.comments = comments
        self.updated = updated
        self.created = created
        self.pager_id = pager_id
        self.liked = liked
        self.checksum = checksum
        self.is_dynamic_shipping_fee = is_dynamic_shipping_fee
        self.application_attributes = application_attributes
        self.is_shop_item = is_shop_item
        self.is_anonymous_shipping = is_anonymous_shipping
        self.is_web_visible = is_web_visible
        self.is_offerable = is_offerable
        self.organizational_user_status = organizational_user_status
        self.is_organizational_user = is_organizational_user
        self.is_stock_item = is_stock_item
        self.is_cancelable = is_cancelable
        self.shipped_by_worker = shipped_by_worker
        self.has_additional_service = has_additional_service
        self.has_like_list = has_like_list
        self.is_offerable_v2 = is_offerable_v2
