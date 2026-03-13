"""Note classes for storing notes with metadata."""

from datetime import datetime
from uuid import UUID, uuid4

from app.message_texts import (
    INVALID_NOTE_TAGS_FORMAT,
    INVALID_NOTE_TEXT_FORMAT,
    INVALID_NOTE_TITLE_FORMAT,
)
from app.validators import is_valid_note_tag, is_valid_note_text, is_valid_note_title

from .exceptions import InvalidNoteError
from .field import Field


# pylint: disable=too-few-public-methods
class NoteText(Field):
    """Field class for note text with validation."""

    def __init__(self, value: str) -> None:
        """Initialize note text field with validation.

        Args:
            value: Note text content (1-500 characters).
        """
        trimmed = value.strip()

        if not is_valid_note_text(trimmed):
            raise InvalidNoteError(INVALID_NOTE_TEXT_FORMAT)

        super().__init__(trimmed)


# pylint: disable=too-few-public-methods
class NoteTitle(Field):
    """Field class for note title with validation."""

    def __init__(self, value: str) -> None:
        """Initialize note title field with validation."""

        trimmed = value.strip()

        if not is_valid_note_title(trimmed):
            raise InvalidNoteError(INVALID_NOTE_TITLE_FORMAT)

        super().__init__(trimmed)


class Note:
    """Class for storing a note with metadata and unique UUID identifier."""

    def __init__(self, title: str, text: str, tags: list[str] | None = None) -> None:
        """Initialize note with title, text, and optional tags.

        Args:
            title: Short note title.
            text: Main note text.
            tags: Optional list of note tags.
        """

        now = datetime.now()

        self.id: UUID = uuid4()
        self.title: NoteTitle = NoteTitle(title)
        self.text: NoteText = NoteText(text)
        self.tags: list[str] = self.normalize_tags(tags or [])
        self.created_at: datetime = now
        self.updated_at: datetime = now

    @staticmethod
    def normalize_tags(tags: list[str]) -> list[str]:
        """Normalize tags while preserving user-visible casing."""

        normalized_tags: list[str] = []
        seen: set[str] = set()

        for tag in tags:
            trimmed = tag.strip()

            if not is_valid_note_tag(trimmed):
                raise InvalidNoteError(INVALID_NOTE_TAGS_FORMAT)

            normalized_key = trimmed.lower()
            if normalized_key in seen:
                continue

            seen.add(normalized_key)
            normalized_tags.append(trimmed)

        return normalized_tags

    def __str__(self) -> str:
        """Return concise string representation of the note."""

        return f"{self.title.value}: {self.text.value}"
