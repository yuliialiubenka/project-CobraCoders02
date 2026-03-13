"""Handler for the search-notes command."""

from colorama import Fore

from app.decorators import colored_output, input_error, validate_args
from app.messages import error_missing_args_search_notes, no_matching_notes_message
from app.models import NotesBook

from .show_notes import format_note_records


@colored_output(success_color=Fore.BLUE, info_color=Fore.BLUE)
@input_error
@validate_args(
    required_count=1,
    normalize_args=True,
    missing_args_message=error_missing_args_search_notes(),
)
def search_notes(args: list[str], notes_book: NotesBook) -> str:
    """
    Search notes across all fields (title, text, tags) with partial match.

    Args:
        args: List of arguments where args[0] is the search query.
        notes_book: NotesBook instance to search.

    Returns:
        Formatted table of matching notes, or no-results message.
    """

    matches = notes_book.search(args[0])

    if not matches:
        return no_matching_notes_message()

    sorted_matches = sorted(matches, key=lambda note: note.created_at)
    return format_note_records(sorted_matches, title="=== Notes Search Results ===")
