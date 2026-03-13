"""Handler for the show-tag command. Displays all notes from NotesBook by tag."""

from colorama import Fore

from app.decorators import colored_output, input_error, validate_args
from app.messages import no_tag_found_message, invalid_tag
from app.models import NotesBook, Note
from app.validators import is_valid_tag

from .show_notes import format_note_records



@colored_output(success_color=Fore.BLUE, info_color=Fore.BLUE)
@input_error
@validate_args(
    required_count=1,
    validators={0: is_valid_tag},
    error_messages={0: invalid_tag()},
    normalize_args=True,
    missing_args_message=invalid_tag(),
)
def search_tag(args: list[str], notes_book: NotesBook) -> str:
    """
    Display all notes with enter tag.

    """
    matches: list[Note] = notes_book.search_tag(args[0])

    # matches = notes_book.search_tag()

    if not matches:
        return no_tag_found_message()

    sorted_notes = sorted(matches, key=lambda note: note.created_at)
    return format_note_records(sorted_notes)