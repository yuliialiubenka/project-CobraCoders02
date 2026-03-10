"""Address field class for contact addresses."""

from app.message_texts import INVALID_ADDRESS_FORMAT
from app.validators import is_valid_address

from .exceptions import InvalidAddressError
from .field import Field


# pylint: disable=too-few-public-methods
class Address(Field):
    """Class for storing address with basic validation."""

    def __init__(self, value: str) -> None:
        """Initialize address field with validation and normalization."""

        normalized = value.strip()

        if not is_valid_address(normalized):
            raise InvalidAddressError(INVALID_ADDRESS_FORMAT)

        super().__init__(normalized)
