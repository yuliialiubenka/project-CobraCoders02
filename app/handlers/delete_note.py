"""Handler for the delete-note command."""

from app.decorators import colored_output, input_error, validate_args
from app.messages import (
    error_invalid_note_title_format,
    error_missing_args_delete_note,
    note_deleted_message,
    note_not_found_message,
)
from app.models import NotesBook
from app.validators import is_valid_note_title


@colored_output()
@input_error
@validate_args(
    required_count=1,
    validators={0: is_valid_note_title},
    error_messages={0: error_invalid_note_title_format()},
    normalize_args=True,
    missing_args_message=error_missing_args_delete_note(),
)
def delete_note(args: list[str], notes_book: NotesBook) -> str:
    """
    Delete a note from the notes book by title.

    Args:
        args: List of arguments where args[0] is the note title to delete.
        notes_book: NotesBook instance containing notes.

    Returns:
        Success message "Note deleted." if note was deleted.
        "Note not found." if no note with that title exists.

    Example:
        >>> notes_book = NotesBook()
        >>> notes_book.add_note("Plan", "Write tasks")
        >>> delete_note(["Plan"], notes_book)
        "Note deleted."
    """

    title = args[0]
    note = notes_book.find(title)

    if note is None:
        error = ValueError(note_not_found_message())
        error.custom_message = note_not_found_message()
        raise error

    notes_book.delete(note.id)
    return note_deleted_message()
