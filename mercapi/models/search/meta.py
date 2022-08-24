from mercapi.models.base import ResponseModel, Extractors


class Meta(ResponseModel):
    _required_properties = [
        ("nextPageToken", "next_page_token", Extractors.get("nextPageToken")),
        ("previousPageToken", "prev_page_token", Extractors.get("previousPageToken")),
        ("numFound", "num_found", Extractors.get_as("numFound", int)),
    ]
    _optional_properties = []

    def __init__(self, next_page_token: str, prev_page_token: str, num_found: int):
        super().__init__()
        self.next_page_token = next_page_token
        self.prev_page_token = prev_page_token
        self.num_found = num_found
