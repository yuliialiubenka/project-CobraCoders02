"""Persistence helpers for saving and loading the address book."""

import pickle
from uuid import uuid4

from app.models import AddressBook


def _migrate_loaded_book(book: AddressBook) -> AddressBook:
    """Backfill newly added record attributes for older pickle snapshots."""

    needs_rekey = False

    for record in book.data.values():
        if not hasattr(record, "email"):
            record.email = None
        if not hasattr(record, "address"):
            record.address = None
        if not hasattr(record, "id"):
            record.id = uuid4()
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


def save_notes(notes: list[dict], filename: str = "notes.pkl") -> None:
    """
    Save the notes list to a file using pickle serialization.

    Args:
        notes: List of note dicts with "id" (str) and "text" (str) keys.
        filename: The name of the file to save to (default: "notes.pkl").
    """
    with open(filename, "wb") as file:
        pickle.dump(notes, file)


def load_notes(filename: str = "notes.pkl") -> list[dict]:
    """
    Load the notes list from a file using pickle deserialization.

    Args:
        filename: The name of the file to load from (default: "notes.pkl").

    Returns:
        A list of note dicts with "id" (str) and "text" (str). If the file
        does not exist or is invalid, returns an empty list. Legacy pickles
        containing plain strings are migrated to dicts with new UUIDs.
    """
    try:
        with open(filename, "rb") as file:
            loaded = pickle.load(file)
        if not isinstance(loaded, list):
            return []
        result = []
        for item in loaded:
            if isinstance(item, dict) and "id" in item and "text" in item:
                result.append({"id": str(item["id"]), "text": str(item["text"])})
            else:
                result.append({"id": str(uuid4()), "text": str(item)})
        return result
    except (FileNotFoundError, pickle.UnpicklingError, EOFError):
        return []
