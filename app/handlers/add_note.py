"""Handler for the add-note command. Notes are stored via NotesBook."""

from app.decorators import colored_output, input_error
from app.messages import (
    error_duplicate_note_title,
    error_invalid_delimiters_add_note,
    error_invalid_note_tags_format,
    error_invalid_note_text_format,
    error_invalid_note_title_format,
    error_missing_delimiter_add_note,
    error_missing_args_add_note,
    note_added_message,
)
from app.models import NotesBook
from app.validators import is_valid_note_tag, is_valid_note_text, is_valid_note_title


def _raise_input_error(message: str) -> None:
    """Raise a ValueError carrying a user-facing message."""

    error = ValueError(message)
    error.custom_message = message
    raise error


def _parse_tags(raw_tags: str) -> list[str]:
    """Parse comma-separated tag string into a normalized list."""

    if not raw_tags.strip():
        return []

    tags = [tag.strip() for tag in raw_tags.split(",")]

    if any(not tag or not is_valid_note_tag(tag) for tag in tags):
        _raise_input_error(error_invalid_note_tags_format())

    return tags


def _split_note_parts(args: list[str]) -> tuple[str, str, list[str]]:
    """Split add-note arguments into title, text, and optional tags."""

    if len(args) < 3:
        _raise_input_error(error_missing_args_add_note())

    delimiter_indexes = [index for index, value in enumerate(args) if value == "--"]

    if not delimiter_indexes:
        _raise_input_error(error_missing_delimiter_add_note())

    if len(delimiter_indexes) > 2:
        _raise_input_error(error_invalid_delimiters_add_note())

    first_delimiter = delimiter_indexes[0]
    second_delimiter = delimiter_indexes[1] if len(delimiter_indexes) == 2 else None

    title = " ".join(args[:first_delimiter]).strip()
    text_parts = args[first_delimiter + 1 : second_delimiter]
    text = " ".join(text_parts).strip()

    if not title or not text:
        _raise_input_error(error_missing_args_add_note())

    raw_tags = ""
    if second_delimiter is not None:
        raw_tags = " ".join(args[second_delimiter + 1 :]).strip()

    return title, text, _parse_tags(raw_tags)


@colored_output()
@input_error
def add_note(args: list[str], notes_book: NotesBook) -> str:
    """
    Add a note using the format title -- text -- optional comma-separated tags.

    Args:
        args: Raw command arguments after `add-note`.
        notes_book: NotesBook instance for storing notes.

    Returns:
        Success message.
    """

    title, text, tags = _split_note_parts(args)

    if not is_valid_note_title(title):
        return error_invalid_note_title_format()

    if not is_valid_note_text(text):
        return error_invalid_note_text_format()

    if notes_book.find(title) is not None:
        return error_duplicate_note_title(title)

    notes_book.add_note(title, text, tags)
    return note_added_message()
