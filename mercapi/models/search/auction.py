from dataclasses import dataclass
from datetime import datetime

from mercapi.models.base import ResponseModel

@dataclass
class Auction(ResponseModel):
    id_: str
    bid_deadline: datetime
    total_bid: int
    highest_bid: int