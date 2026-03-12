"""Persistence helpers for saving and loading the address book and notes."""

import pickle
from uuid import UUID, uuid4

from app.models import AddressBook, NotesBook, Note


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
    except (FileNotFoundError, pickle.UnpicklingError, EOFError):
        return AddressBook()


def _migrate_loaded_notes(notes_book: NotesBook) -> NotesBook:
    """Backfill UUIDs for legacy notes if needed."""
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
                    note = Note(item["text"])
                    # Preserve old UUID if it exists as string, else generate new
                    if "id" in item:
                        try:
                            note.id = UUID(str(item["id"]))
                        except (ValueError, TypeError):
                            note.id = uuid4()
                    notes_book.data[note.id] = note
                elif isinstance(item, str):
                    # Plain string format
                    note = Note(item)
                    notes_book.data[note.id] = note

        return notes_book

    # FileNotFoundError: file does not exist yet (first app run)
    # pickle.UnpicklingError: file content is not a valid pickle stream
    # EOFError: file is empty/truncated (e.g., interrupted write)
    except (FileNotFoundError, pickle.UnpicklingError, EOFError):
        return NotesBook()