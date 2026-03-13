"""NotesBook class for storing and managing notes."""

from collections import UserDict
from uuid import UUID

from .note import Note


class NotesBook(UserDict):
    """Class for storing notes and managing note collection."""

    def add_note(self, title: str, text: str, tags: list[str] | None = None) -> Note:
        """Add a note and return the created Note.

        Args:
            title: Note title.
            text: Note text content.
            tags: Optional list of tags.

        Returns:
            The newly created Note instance.
        """
        note = Note(title, text, tags)
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

    def find(self, title: str) -> Note | None:
        """Find the first note matching the given title (case-insensitive).

        Args:
            title: Note title to search for.

        Returns:
            The first matching Note if found, None otherwise.
        """
        normalized = title.strip().lower()

        for note in self.data.values():
            if note.title.value.lower() == normalized:
                return note

        return None

    def search(self, query: str) -> list[Note]:
        """Search notes by title, text, or tags.

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
            if normalized_query in note.title.value.lower()
            or normalized_query in note.text.value.lower()
            or any(normalized_query in tag.lower() for tag in note.tags)
        ]
        return matches
