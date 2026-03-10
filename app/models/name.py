"""Name field class for contact names."""

from app.message_texts import INVALID_NAME_FORMAT
from app.validators import is_valid_name

from .exceptions import InvalidNameError
from .field import Field


# pylint: disable=too-few-public-methods
class Name(Field):
    """Class for storing contact name. Required field."""

    def __init__(self, value: str) -> None:
        """Initialize name field with validation."""

        # Validate name format
        if not is_valid_name(value):
            raise InvalidNameError(INVALID_NAME_FORMAT)

        super().__init__(value)
