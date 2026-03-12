"""Tag class for storing tags from notes."""


from app.message_texts import INVALID_TAG_FORMAT
from app.validators import is_valid_tag

from .exceptions import InvalidNoteError
from .field import Field


class TagMatch(Field):
    """Field class for tag with validation."""

    def __init__(self, value: str) -> None:
        """Initialize tag field with validation.

        Args:
            value: tag text content (#).
        """
        trimmed = value.strip()

        if not is_valid_tag(trimmed):
            raise InvalidNoteError(INVALID_TAG_FORMAT)

        super().__init__(trimmed)