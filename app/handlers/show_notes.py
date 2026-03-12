"""Handler for the show-notes command. Displays all notes from NotesBook."""

from colorama import Fore

from app.decorators import colored_output, input_error
from app.messages import no_notes_found_message
from app.models import NotesBook


@colored_output(success_color=Fore.BLUE, info_color=Fore.BLUE)
@input_error
def show_notes(notes_book: NotesBook) -> str:
    """
    Display all notes with their id and text.

    Args:
        notes_book: NotesBook instance containing notes.

    Returns:
        Formatted string with all notes or no-notes-found message.
    """
    if not notes_book.data:
        return no_notes_found_message()

    lines = ["=== Notes ==="]

    for i, note in enumerate(notes_book.data.values(), start=1):
        lines.append(f"  Note {i}: {note.text}")

    return "\n".join(lines)