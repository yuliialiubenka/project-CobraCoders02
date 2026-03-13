"""Handler for sorting notes by tags."""

from app.decorators import colored_output, input_error
from app.models import NotesBook

from .show_notes import format_notes


@colored_output()
@input_error
def sort_notes(notes_book: NotesBook) -> str:
    """Sort notes alphabetically by their tags."""

    return format_notes(notes_book.sort_by_tags(), title="=== Notes Sorted By Tags ===")
