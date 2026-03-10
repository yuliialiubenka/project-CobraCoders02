"""Birthday field class for storing contact birthdays."""

from datetime import datetime

from app.message_texts import INVALID_BIRTHDAY_FORMAT
from app.validators import is_valid_birthday

from .exceptions import InvalidBirthdayError
from .field import Field


# pylint: disable=too-few-public-methods
class Birthday(Field):
    """Class for storing birthday with validation (DD.MM.YYYY format)."""

    def __init__(self, value: str) -> None:
        """Initialize birthday field with validation and conversion to datetime."""

        # First validate the input format
        if not is_valid_birthday(value):
            raise InvalidBirthdayError(INVALID_BIRTHDAY_FORMAT)

        # Then convert to datetime object
        date_obj = self._parse_date(value)
        super().__init__(value)
        self.date: datetime = date_obj

    @staticmethod
    def _parse_date(birthday: str) -> datetime:
        """Parse date string DD.MM.YYYY to datetime object."""

        return datetime.strptime(birthday, "%d.%m.%Y")
