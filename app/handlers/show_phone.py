from app.decorators import colored_output, input_error, validate_args
from app.messages import error_invalid_name_format, error_missing_args_phone
from app.models import AddressBook
from app.validators import is_valid_name


@colored_output()
@input_error
@validate_args(
    required_count=1,
    validators={0: is_valid_name},
    error_messages={0: error_invalid_name_format()},
    normalize_args=True,
    missing_args_message=error_missing_args_phone(),
)
def show_phone(args: list[str], book: AddressBook) -> str:
    """
    Retrieve and return phone numbers for a specific contact.

    Looks up a contact by name and returns their phone numbers.

    Args:
        args: List of arguments where args[0] is the contact name to look up.
              Must contain at least 1 element.
        book: AddressBook instance containing contact information.

    Returns:
        The contact's phone numbers as a formatted string.

    Raises:
        IndexError: If no arguments provided (empty args list).
        KeyError: If the named contact does not exist in the address book.

    Example:
        >>> book = AddressBook()
        >>> record = Record("John")
        >>> record.add_phone("0987654321")
        >>> book.add_record(record)
        >>> show_phone(["John"], book)
        "John: 0987654321"
    """

    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError

    phones = "; ".join(p.value for p in record.phones)
    return f"{name}: {phones}"
