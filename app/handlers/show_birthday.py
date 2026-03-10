from app.decorators import colored_output, input_error, validate_args
from app.messages import error_invalid_name_format
from app.models import AddressBook
from app.validators import is_valid_name


@colored_output()
@input_error
@validate_args(
    required_count=1,
    validators={0: is_valid_name},
    error_messages={0: error_invalid_name_format()},
    normalize_args=True,
)
def show_birthday(args: list[str], book: AddressBook) -> str:
    """
    Show birthday for a specific contact.

    Args:
        args: List where args[0] is the contact name.
        book: AddressBook instance.

    Returns:
        Birthday in format "Name: DD.MM.YYYY".

    Raises:
        KeyError: If contact not found or has no birthday.

    Example:
        >>> book = AddressBook()
        >>> record = Record("John")
        >>> record.add_birthday("15.03.1990")
        >>> book.add_record(record)
        >>> show_birthday(["John"], book)
        "John: 15.03.1990"
    """

    name = args[0]
    record = book.find(name)

    if record is None or record.birthday is None:
        raise KeyError

    return f"{name}: {record.birthday.value}"
