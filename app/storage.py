"""Persistence helpers for saving and loading the address book."""

import pickle

from app.models import AddressBook


def _migrate_loaded_book(book: AddressBook) -> AddressBook:
    """Backfill newly added record attributes for older pickle snapshots."""

    for record in book.data.values():
        if not hasattr(record, "email"):
            record.email = None
        if not hasattr(record, "address"):
            record.address = None

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
