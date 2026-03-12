"""Handler for the show-tag command. Displays all notes from NotesBook by tag."""

from colorama import Fore

from app.decorators import colored_output, input_error
from app.messages import no_notes_found_message
from app.models import NotesBook


@colored_output(success_color=Fore.BLUE, info_color=Fore.BLUE)
@input_error
def shearch_tag(notes_book: NotesBook) -> str:
    """
    Display all notes with their id and text.

    Args:
        notes_book: NotesBook instance containing notes.

    Returns:
        Formatted string with all notes or no-notes-found message.
    """
    pass