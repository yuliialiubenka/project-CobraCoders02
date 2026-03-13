"""NotesBook class for storing and managing notes."""

from collections import UserDict
from uuid import UUID

from .note import Note


class NotesBook(UserDict):
    """Class for storing notes and managing note collection."""

    def add_note(self, text: str, tags: list[str] | None = None) -> Note:
        """Add a note and return the created Note.

        Args:
            text: Note text content.
            tags: Optional note tags.

        Returns:
            The newly created Note instance.
        """
        note = Note(text, tags)
        self.data[note.id] = note

        return note

    def delete(self, note_id: UUID) -> bool:
        """Delete a note by UUID.

        Args:
            note_id: UUID of the note to delete.

        Returns:
            True if note was deleted, False if not found.
        """
        if note_id in self.data:
            del self.data[note_id]
            return True
        return False

    def find(self, note_id: UUID) -> Note | None:
        """Find a note by UUID.

        Args:
            note_id: UUID of the note to find.

        Returns:
            The Note if found, None otherwise.
        """
        return self.data.get(note_id)

    def search(self, query: str) -> list[Note]:
        """Search notes by text content or tags.

        Args:
            query: Search query string.

        Returns:
            List of Note instances matching the query.
        """
        normalized_query = query.strip().lower()

        if not normalized_query:
            return []

        matches = [
            note
            for note in self.data.values()
            if normalized_query in note.text.value.lower()
            or normalized_query in note.tags
        ]
        return matches

    def search_by_tag(self, tag: str) -> list[Note]:
        """Search notes by a single tag."""

        normalized_tag = Note.normalize_tag(tag)
        return [
            note for note in self.data.values() if normalized_tag in note.tags
        ]

    def sort_by_tags(self) -> list[Note]:
        """Return notes sorted alphabetically by their tags."""

        return sorted(
            self.data.values(),
            key=lambda note: (not note.tags, note.tags, note.text.value.lower()),
        )