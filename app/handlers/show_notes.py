"""Handler for the show-notes command. Displays all notes from NotesBook."""

from datetime import datetime

from colorama import Fore

from app.decorators import colored_output, input_error
from app.messages import no_notes_found_message
from app.models import Note, NotesBook


def _format_timestamp(timestamp: datetime) -> str:
    """Format note timestamps for CLI output."""

    return timestamp.strftime("%d.%m.%Y %H:%M")


def format_note_records(
    notes: list[Note],
    title: str = "=== Notes List ===",
) -> str:
    """Format notes as a vertical table similar to contacts output."""

    if not notes:
        return no_notes_found_message()

    all_labels = ["Title", "Text", "Tags", "Date"]
    global_col1_width = max(len(label) for label in all_labels)
    all_tables: list[str] = []

    for note in notes:
        date_value = _format_timestamp(
            note.updated_at if note.updated_at != note.created_at else note.created_at
        )
        rows = [
            ("Title", note.title.value),
            ("Text", note.text.value),
        ]

        if note.tags:
            rows.append(("Tags", ", ".join(note.tags)))

        rows.append(("Date", date_value))

        col2_width = max(len(value) for _, value in rows)
        table_lines = [
            f"{label:<{global_col1_width}} | {value:<{col2_width}}"
            for label, value in rows
        ]
        all_tables.append("\n".join(table_lines))

    separator = " " * len(title)
    return f"{title}\n{separator}\n" + "\n\n".join(all_tables)


@colored_output(success_color=Fore.BLUE, info_color=Fore.BLUE)
@input_error
def show_notes(notes_book: NotesBook) -> str:
    """
    Display all notes in a formatted vertical table.

    Notes are sorted oldest-first so the most recently added note
    appears closest to the input prompt.

    Args:
        notes_book: NotesBook instance containing notes.

    Returns:
        Formatted vertical table string with note entries.
    """
    if not notes_book.data:
        return no_notes_found_message()

    sorted_notes = sorted(notes_book.data.values(), key=lambda note: note.created_at)
    return format_note_records(sorted_notes)
