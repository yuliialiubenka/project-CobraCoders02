"""Handler for the add-note command. Notes are stored via NotesBook."""

from app.decorators import colored_output, input_error
from app.messages import (
    error_invalid_note_format,
    error_invalid_tag_format,
    error_missing_args_add_note,
    note_added_message,
)
from app.models import InvalidNoteError, NotesBook
from app.validators import is_valid_note


def _parse_note_args(args: list[str]) -> tuple[str, list[str]] | None:
    """Split add-note arguments into note text and optional tags."""

    if not args:
        return None

    if "--tags" not in args:
        return " ".join(args).strip(), []

    separator_index = args.index("--tags")
    note_text = " ".join(args[:separator_index]).strip()
    raw_tags = " ".join(args[separator_index + 1 :]).strip()

    if not note_text or not raw_tags:
        return None

    tag_items = [tag.strip() for tag in raw_tags.split(",")]
    return note_text, tag_items


@colored_output()
@input_error
def add_note(args: list[str], notes_book: NotesBook) -> str:
    """
    Add a standalone note with optional tags.

    Args:
        args: Note text and optional `--tags tag1,tag2` suffix.
        notes_book: NotesBook instance for storing notes.

    Returns:
        Success message.
    """
    parsed_args = _parse_note_args(args)

    if not parsed_args:
        return error_missing_args_add_note()

    note_text, tags = parsed_args

    if not is_valid_note(note_text):
        return error_invalid_note_format()

    try:
        notes_book.add_note(note_text, tags)
    except InvalidNoteError:
        return error_invalid_tag_format()

    return note_added_message()