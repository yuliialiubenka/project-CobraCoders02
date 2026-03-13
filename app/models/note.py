"""Note class for storing text notes."""

from uuid import UUID, uuid4

from app.message_texts import INVALID_NOTE_FORMAT, INVALID_TAG_FORMAT
from app.validators import is_valid_note, is_valid_tag

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

    def __init__(self, text: str, tags: list[str] | None = None) -> None:
        """Initialize note with text.

        Args:
            text: Note text content (1-50 characters).
            tags: Optional note tags.
        """

        self.id: UUID = uuid4()
        self.text: NoteText = NoteText(text)
        self.tags: list[str] = self.normalize_tags(tags)

    @staticmethod
    def normalize_tag(tag: str) -> str:
        """Normalize and validate a single tag."""

        normalized = tag.strip().lstrip("#").lower()

        if not is_valid_tag(normalized):
            raise InvalidNoteError(INVALID_TAG_FORMAT)

        return normalized

    @classmethod
    def normalize_tags(cls, tags: list[str] | None) -> list[str]:
        """Normalize tags, keeping insertion order and removing duplicates."""

        if not tags:
            return []

        normalized_tags: list[str] = []
        seen_tags: set[str] = set()

        for tag in tags:
            normalized_tag = cls.normalize_tag(tag)

            if normalized_tag not in seen_tags:
                normalized_tags.append(normalized_tag)
                seen_tags.add(normalized_tag)

        return normalized_tags

    def format_tags(self) -> str:
        """Return tags in a user-friendly format."""

        if not self.tags:
            return "no tags"

        return ", ".join(f"#{tag}" for tag in self.tags)

    def __str__(self) -> str:
        """Return string representation of the note."""

        return f"[{self.id}] {self.text} | tags: {self.format_tags()}"