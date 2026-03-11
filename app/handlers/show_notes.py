"""Handler for the show-notes command. Displays all notes (id and text) from notes.pkl."""

from colorama import Fore

from app.decorators import colored_output, input_error
from app.messages import no_notes_found_message
from app.models import AddressBook
from app.storage import load_notes


@colored_output(success_color=Fore.BLUE, info_color=Fore.BLUE)
@input_error
def show_notes(book: AddressBook) -> str:
    """Display all notes with their id and text. Book is unused; notes are stored separately."""
    notes = load_notes()
    if not notes:
        return no_notes_found_message()
    lines = ["=== Notes ==="]
    for note in notes:
        nid = note.get("id", "")
        text = note.get("text", "")
        lines.append(f"  [{nid}]  {text}")
    return "\n".join(lines)
