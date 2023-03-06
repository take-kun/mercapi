from dataclasses import dataclass

from mercapi.models.base import ResponseModel


@dataclass
class Meta(ResponseModel):
    next_page_token: str
    prev_page_token: str
    num_found: int
