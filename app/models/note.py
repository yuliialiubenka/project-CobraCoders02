"""Note class for storing text notes."""

from uuid import UUID, uuid4

from app.message_texts import INVALID_NOTE_FORMAT
from app.validators import is_valid_note

from .exceptions import InvalidNoteError
from .field import Field


# pylint: disable=too-few-public-methods
class NoteText(Field):
    """Field class for note text with validation."""

    def __init__(self, value: str) -> None:
        """Initialize note text field with validation.

        Args:
            value: Note text content (1-50 characters).
        """
        trimmed = value.strip()

        if not is_valid_note(trimmed):
            raise InvalidNoteError(INVALID_NOTE_FORMAT)

        super().__init__(trimmed)


class Note:
    """Class for storing a text note with unique UUID identifier."""

    def __init__(self, text: str) -> None:
        """Initialize note with text.

        Args:
            text: Note text content (1-50 characters).
        """

        self.id: UUID = uuid4()
        self.text: NoteText = NoteText(text)

    def __str__(self) -> str:
        """Return string representation of the note."""

        return f"[{self.id}]  {self.text}"