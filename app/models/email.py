"""Email field class for contact email addresses."""

from app.message_texts import INVALID_EMAIL_FORMAT
from app.validators import is_valid_email

from .exceptions import InvalidEmailError
from .field import Field


# pylint: disable=too-few-public-methods
class Email(Field):
    """Class for storing email with validation."""

    def __init__(self, value: str) -> None:
        """Initialize email field with validation and normalization."""

        normalized = value.strip().lower()

        if not is_valid_email(normalized):
            raise InvalidEmailError(INVALID_EMAIL_FORMAT)

        super().__init__(normalized)
