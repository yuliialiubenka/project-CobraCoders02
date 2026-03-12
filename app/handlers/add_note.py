"""Handler for the add-note command. Notes are stored via NotesBook."""

from app.decorators import colored_output, input_error, validate_args
from app.messages import (
    error_invalid_note_format,
    error_missing_args_add_note,
    note_added_message,
)
from app.models import NotesBook
from app.validators import is_valid_note


@colored_output()
@input_error
@validate_args(
    required_count=1,
    validators={0: is_valid_note},
    error_messages={0: error_invalid_note_format()},
    normalize_args=True,
    missing_args_message=error_missing_args_add_note(),
)
def add_note(args: list[str], notes_book: NotesBook) -> str:
    """
    Add a standalone note (1-50 characters). Stored in NotesBook.

    Args:
        args: List where args[0] is the validated, normalized note text.
        notes_book: NotesBook instance for storing notes.

    Returns:
        Success message.
    """
    notes_book.add_note(args[0])
    return note_added_message()
	