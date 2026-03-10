from app.decorators import colored_output, input_error, validate_args
from app.messages import (
    error_invalid_name_format,
    error_invalid_phone_format,
    error_missing_args_change,
)
from app.models import AddressBook
from app.validators import is_valid_name, is_valid_phone


@colored_output()
@input_error
@validate_args(
    required_count=3,
    validators={0: is_valid_name, 1: is_valid_phone, 2: is_valid_phone},
    error_messages={
        0: error_invalid_name_format(),
        1: error_invalid_phone_format(),
        2: error_invalid_phone_format(),
    },
    normalize_args=True,
    missing_args_message=error_missing_args_change(),
)
def change_contact(args: list[str], book: AddressBook) -> str:
    """
    Change phone number for an existing contact.

    Updates the phone number for a contact that already exists in the address book.

    Args:
        args: List where args[0] is contact name, args[1] is old phone,
              args[2] is new phone. Must contain at least 3 elements.
        book: AddressBook instance containing existing contact information.

    Returns:
        Success message "Contact updated." if contact exists and was updated.

    Raises:
        ValueError: If insufficient arguments provided (less than 3).
        KeyError: If the named contact does not exist in the address book.

    Example:
        >>> book = AddressBook()
        >>> record = Record("John")
        >>> record.add_phone("0987654321")
        >>> book.add_record(record)
        >>> change_contact(["John", "0987654321", "0670001122"], book)
        "Contact updated."
    """

    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_phone(old_phone, new_phone)
    return "Contact updated."
