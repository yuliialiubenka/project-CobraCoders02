"""Handler for the add-note command. Notes are stored separately from contacts (notes.pkl)."""

import uuid

from app.decorators import colored_output, input_error
from app.messages import (
    error_invalid_note_format,
    error_missing_args_add_note,
    note_added_message,
)
from app.models import AddressBook
from app.storage import load_notes, save_notes
from app.validators import is_valid_note


@colored_output()
@input_error
def add_note(args: list[str], book: AddressBook) -> str:
    """Add a standalone note (max 50 characters). Stored in notes.pkl with a UUID4 id."""
    if not args:
        return error_missing_args_add_note()

    note_text = " ".join(args).strip()
    if not note_text:
        return error_missing_args_add_note()

    if not is_valid_note(note_text):
        return error_invalid_note_format()

    notes = load_notes()
    notes.append({"id": str(uuid.uuid4()), "text": note_text})
    save_notes(notes)
    return note_added_message()
