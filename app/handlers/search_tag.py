"""Handler for the show-tag command. Displays all notes from NotesBook by tag."""

from colorama import Fore

from app.decorators import colored_output, input_error
from app.messages import no_tag_found_message
from app.models import NotesBook, Note

from .show_notes import format_note_records



@colored_output(success_color=Fore.BLUE, info_color=Fore.BLUE)
@input_error
def search_tag(notes_book: NotesBook, tag: str) -> str:
    """
    Display all notes with enter tag.

    """
    matches: list[Note] = notes_book.search_tag(tag)

    matches = notes_book.search_tag()

    if not matches:
        return no_tag_found_message()

    sorted_notes = sorted(matches, key=lambda note: note.created_at)
    return format_note_records(sorted_notes)