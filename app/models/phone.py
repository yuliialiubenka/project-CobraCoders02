"""Phone field class for phone numbers."""

import re

from app.message_texts import INVALID_PHONE_FORMAT
from app.validators import is_valid_phone

from .exceptions import InvalidPhoneError
from .field import Field


# pylint: disable=too-few-public-methods
class Phone(Field):
    """Class for storing phone numbers with validation (local 10 digits)."""

    def __init__(self, value: str) -> None:
        """Initialize phone field with validation and normalization."""

        # First validate the input format (local only)
        if not is_valid_phone(value):
            raise InvalidPhoneError(INVALID_PHONE_FORMAT)

        # Then normalize it to local format (10 digits)
        normalized: str = self._normalize(value)
        super().__init__(normalized)

    @staticmethod
    def _normalize(phone: str) -> str:
        """Extract digits to get local format (10 digits)."""

        if not isinstance(phone, str):
            return ""

        digits_only: str = re.sub(r"\D", "", phone)

        return digits_only
