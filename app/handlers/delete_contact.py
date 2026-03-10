from app.decorators import colored_output, input_error, validate_args
from app.messages import (
    contact_deleted_message,
    error_invalid_name_format,
    error_missing_args_delete,
)
from app.models import AddressBook
from app.validators import is_valid_name


@colored_output()
@input_error
@validate_args(
    required_count=1,
    validators={0: is_valid_name},
    error_messages={0: error_invalid_name_format()},
    normalize_args=True,
    missing_args_message=error_missing_args_delete(),
)
def delete_contact(args: list[str], book: AddressBook) -> str:
    """
    Delete a contact from the address book.

    Removes an entire contact record by name from the address book.

    Args:
        args: List of arguments where args[0] is the contact name to delete.
              Must contain at least 1 element.
        book: AddressBook instance containing contact information.

    Returns:
        Success message "Contact deleted." if contact was deleted.

    Raises:
        KeyError: If the named contact does not exist in the address book.

    Example:
        >>> book = AddressBook()
        >>> record = Record("John")
        >>> book.add_record(record)
        >>> delete_contact(["John"], book)
        "Contact deleted."
    """

    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError

    book.delete(name)
    return contact_deleted_message()
