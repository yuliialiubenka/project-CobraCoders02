"""Handler for searching notes by tag."""

from app.decorators import colored_output, input_error, validate_args
from app.messages import (
    error_invalid_tag_format,
    error_missing_args_search_notes,
    no_matching_notes_message,
)
from app.models import NotesBook
from app.validators import is_valid_tag

from .show_notes import format_notes


@colored_output()
@input_error
@validate_args(
    required_count=1,
    validators={0: is_valid_tag},
    error_messages={0: error_invalid_tag_format()},
    normalize_args=True,
    missing_args_message=error_missing_args_search_notes(),
)
def search_notes(args: list[str], notes_book: NotesBook) -> str:
    """Search notes by a single tag."""

    matches = notes_book.search_by_tag(args[0])

    if not matches:
        return no_matching_notes_message()

    return format_notes(matches, title="=== Notes Found By Tag ===")
