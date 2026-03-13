"""Persistence helpers for saving and loading the address book and notes."""

from datetime import datetime
import pickle
from uuid import UUID, uuid4

from app.models import AddressBook, NotesBook, Note
from app.models.note import NoteText, NoteTitle


def _build_legacy_note_title(text: str) -> str:
    """Generate a fallback title for legacy notes that only stored text."""

    normalized_text = " ".join(str(text).split())

    if not normalized_text:
        return "Untitled"

    if len(normalized_text) <= 50:
        return normalized_text

    return normalized_text[:47].rstrip() + "..."


def _coerce_note_tags(tags: object) -> list[str]:
    """Normalize tags loaded from legacy note formats."""

    if tags is None:
        return []

    if isinstance(tags, str):
        raw_tags = [tag.strip() for tag in tags.split(",")]
    elif isinstance(tags, (list, tuple, set)):
        raw_tags = [str(tag).strip() for tag in tags]
    else:
        return []

    return Note.normalize_tags([tag for tag in raw_tags if tag])


def _coerce_note_datetime(value: object, fallback: datetime) -> datetime:
    """Convert legacy timestamp values to datetime when possible."""

    if isinstance(value, datetime):
        return value

    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return fallback

    return fallback


def _migrate_loaded_book(book: AddressBook) -> AddressBook:
    """Backfill newly added record attributes for older pickle snapshots."""

    needs_rekey = False

    for key, record in list(book.data.items()):
        if not hasattr(record, "email"):
            record.email = None
        if not hasattr(record, "address"):
            record.address = None
        if not hasattr(record, "id"):
            record.id = uuid4()
            needs_rekey = True
        else:
            try:
                record.id = UUID(str(record.id))
            except (ValueError, TypeError):
                record.id = uuid4()
                needs_rekey = True

        if key != record.id:
            needs_rekey = True

    if needs_rekey:
        book.data = {record.id: record for record in book.data.values()}

    return book


def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    """
    Save the address book to a file using pickle serialization.

    Args:
        book: The AddressBook instance to save.
        filename: The name of the file to save to (default: "addressbook.pkl").
    """
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    """
    Load the address book from a file using pickle deserialization.

    Args:
        filename: The name of the file to load from (default: "addressbook.pkl").

    Returns:
        An AddressBook instance. If the file does not exist or is invalid,
        returns a new empty AddressBook.
    """
    try:
        with open(filename, "rb") as file:
            loaded_book = pickle.load(file)

        if not isinstance(loaded_book, AddressBook):
            return AddressBook()

        return _migrate_loaded_book(loaded_book)

    # FileNotFoundError: file does not exist yet (first app run)
    # pickle.UnpicklingError: file content is not a valid pickle stream
    # EOFError: file is empty/truncated (e.g., interrupted write)
    # AttributeError/ModuleNotFoundError/ImportError: legacy pickle references
    # classes that no longer exist in current code.
    except (
        FileNotFoundError,
        pickle.UnpicklingError,
        EOFError,
        AttributeError,
        ModuleNotFoundError,
        ImportError,
    ):
        return AddressBook()


def _migrate_loaded_notes(notes_book: NotesBook) -> NotesBook:
    """Backfill fields for legacy notes so current handlers can use them safely."""

    needs_rekey = False

    for key, note in list(notes_book.data.items()):
        if not hasattr(note, "id"):
            note.id = uuid4()
            needs_rekey = True
        else:
            try:
                note.id = UUID(str(note.id))
            except (ValueError, TypeError):
                note.id = uuid4()
                needs_rekey = True

        raw_title = getattr(note, "title", None)
        raw_text = getattr(note, "text", None)

        if isinstance(raw_text, NoteText):
            text_value = raw_text.value
        else:
            text_value = str(getattr(raw_text, "value", raw_text or "Legacy note"))

        if isinstance(raw_title, NoteTitle):
            title_value = raw_title.value
        else:
            title_value = str(
                getattr(
                    raw_title,
                    "value",
                    raw_title or _build_legacy_note_title(text_value),
                )
            )

        note.title = NoteTitle(title_value)
        note.text = NoteText(text_value)
        note.tags = _coerce_note_tags(getattr(note, "tags", []))

        created_at = _coerce_note_datetime(
            getattr(note, "created_at", None), datetime.now()
        )
        updated_at = _coerce_note_datetime(
            getattr(note, "updated_at", None), created_at
        )

        note.created_at = created_at
        note.updated_at = updated_at

        if key != note.id:
            needs_rekey = True

    if needs_rekey:
        notes_book.data = {note.id: note for note in notes_book.data.values()}

    return notes_book


def save_notes(notes_book: NotesBook, filename: str = "notes.pkl") -> None:
    """
    Save the notes book to a file using pickle serialization.

    Args:
        notes_book: The NotesBook instance to save.
        filename: The name of the file to save to (default: "notes.pkl").
    """
    with open(filename, "wb") as file:
        pickle.dump(notes_book, file)


def load_notes(filename: str = "notes.pkl") -> NotesBook:
    """
    Load the notes book from a file using pickle deserialization.

    Args:
        filename: The name of the file to load from (default: "notes.pkl").

    Returns:
        A NotesBook instance. If the file does not exist or is invalid,
        returns a new empty NotesBook. Legacy pickles containing plain
        lists of strings or dicts are migrated to NotesBook.
    """
    try:
        with open(filename, "rb") as file:
            loaded = pickle.load(file)

        # If already NotesBook, return it
        if isinstance(loaded, NotesBook):
            return _migrate_loaded_notes(loaded)

        # Else, migrate legacy format (list of dicts or strings)
        notes_book = NotesBook()

        if isinstance(loaded, list):
            for item in loaded:
                if isinstance(item, dict) and "text" in item:
                    title = item.get("title") or _build_legacy_note_title(item["text"])
                    text = str(item["text"])
                    tags = _coerce_note_tags(item.get("tags", []))
                    note = Note(title, text, tags)
                    # Preserve old UUID if it exists as string, else generate new
                    if "id" in item:
                        try:
                            note.id = UUID(str(item["id"]))
                        except (ValueError, TypeError):
                            note.id = uuid4()
                    note.created_at = _coerce_note_datetime(
                        item.get("created_at"), note.created_at
                    )
                    note.updated_at = _coerce_note_datetime(
                        item.get("updated_at"), note.created_at
                    )
                    notes_book.data[note.id] = note
                elif isinstance(item, str):
                    # Plain string format
                    note = Note(_build_legacy_note_title(item), item)
                    notes_book.data[note.id] = note

        return _migrate_loaded_notes(notes_book)

    # FileNotFoundError: file does not exist yet (first app run)
    # pickle.UnpicklingError: file content is not a valid pickle stream
    # EOFError: file is empty/truncated (e.g., interrupted write)
    # AttributeError/ModuleNotFoundError/ImportError: legacy pickle references
    # classes that no longer exist in current code.
    except (
        FileNotFoundError,
        pickle.UnpicklingError,
        EOFError,
        AttributeError,
        ModuleNotFoundError,
        ImportError,
    ):
        return NotesBook()
