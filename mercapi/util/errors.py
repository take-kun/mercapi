from typing import Any, Dict, List, Optional


class MercapiError(Exception):
    pass


class ParseAPIResponseError(MercapiError):
    pass


class IncorrectRequestError(MercapiError):
    pass


class APIError(MercapiError):
    NOT_FOUND_CODES = frozenset(
        {
            "RecordNotFoundException",
            "NotFoundException",
            "InvisibleItemException",
            "UserNotFoundException",
        }
    )

    def __init__(
        self,
        status_code: int,
        errors: Optional[List[Dict[str, Any]]] = None,
    ):
        self.status_code = status_code
        self.errors = errors or []

        first_error = self.errors[0] if self.errors else {}
        self.code: Optional[str] = first_error.get("code")
        self.message: Optional[str] = first_error.get("message")

        description = f"HTTP {status_code}"
        if self.code:
            description += f" {self.code}"
        if self.message:
            description += f": {self.message}"

        super().__init__(description)

    @property
    def is_not_found(self) -> bool:
        """Whether the requested entity is missing or has been removed."""
        return self.status_code == 404 or self.code in self.NOT_FOUND_CODES
