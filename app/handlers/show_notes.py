"""Handler for the show-notes command. Displays all notes from NotesBook."""

from colorama import Fore

from app.decorators import colored_output, input_error
from app.messages import no_notes_found_message
from app.models import Note, NotesBook


def format_notes(notes: list[Note], title: str = "=== Notes ===") -> str:
    """Format a list of notes for CLI output."""

    if not notes:
        return no_notes_found_message()

    lines = [title]

    for i, note in enumerate(notes, start=1):
        lines.append(f"  Note {i}: {note}")

    return "\n".join(lines)


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
    return format_notes(list(notes_book.data.values()))