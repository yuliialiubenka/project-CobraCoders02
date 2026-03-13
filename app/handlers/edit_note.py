"""Handler for the edit-note command. Updates note text and updates timestamp."""

from datetime import datetime

from app.decorators import colored_output, input_error
from app.messages import (
    error_invalid_delimiters_edit_note,
    error_invalid_note_text_format,
    error_invalid_note_title_format,
    error_missing_delimiter_edit_note,
    error_missing_args_edit_note,
    note_not_found_message,
    note_updated_message,
)
from app.models import NotesBook
from app.models.note import NoteText
from app.validators import is_valid_note_text, is_valid_note_title


def _raise_input_error(message: str) -> None:
    """Raise a ValueError carrying a user-facing message."""

    error = ValueError(message)
    error.custom_message = message
    raise error


def _split_edit_note_parts(args: list[str]) -> tuple[str, str]:
    """Split edit-note arguments into title and new text."""

    if len(args) < 3:
        _raise_input_error(error_missing_args_edit_note())

    delimiter_indexes = [index for index, value in enumerate(args) if value == "--"]

    if not delimiter_indexes:
        _raise_input_error(error_missing_delimiter_edit_note())

    if len(delimiter_indexes) != 1:
        _raise_input_error(error_invalid_delimiters_edit_note())

    first_delimiter = delimiter_indexes[0]

    title = " ".join(args[:first_delimiter]).strip()
    text = " ".join(args[first_delimiter + 1 :]).strip()

    if not title or not text:
        _raise_input_error(error_missing_args_edit_note())

    return title, text


@colored_output()
@input_error
def edit_note(args: list[str], notes_book: NotesBook) -> str:
    """
    Edit a note using the format title -- new text.

    Args:
        args: Raw command arguments after `edit-note`.
        notes_book: NotesBook instance for storing notes.

    Returns:
        Success message if note was updated, error message otherwise.
    """

    title, text = _split_edit_note_parts(args)

    if not is_valid_note_title(title):
        return error_invalid_note_title_format()

    if not is_valid_note_text(text):
        return error_invalid_note_text_format()

    note = notes_book.find(title)
    if note is None:
        return note_not_found_message()

    # Update text and timestamp
    note.text = NoteText(text)
    note.updated_at = datetime.now()

    return note_updated_message()
