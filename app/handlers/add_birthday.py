from app.decorators import colored_output, input_error, validate_args
from app.messages import (
    birthday_added_message,
    error_invalid_birthday_format,
    error_invalid_name_format,
)
from app.models import AddressBook
from app.validators import is_valid_birthday, is_valid_name


@colored_output()
@input_error
@validate_args(
    required_count=2,
    validators={0: is_valid_name, 1: is_valid_birthday},
    error_messages={
        0: error_invalid_name_format(),
        1: error_invalid_birthday_format(),
    },
    normalize_args=True,
)
def add_birthday(args: list[str], book: AddressBook) -> str:
    """
    Add a birthday to an existing contact.

    Args:
        args: List where args[0] is contact name and args[1] is birthday (DD.MM.YYYY).
        book: AddressBook instance.

    Returns:
        Success message "Birthday added." if operation succeeded.

    Raises:
        ValueError: If invalid arguments or contact not found.

    Example:
        >>> book = AddressBook()
        >>> record = Record("John")
        >>> book.add_record(record)
        >>> add_birthday(["John", "15.03.1990"], book)
        "Birthday added."
    """

    name, birthday = args
    record = book.find(name)

    if record is None:
        raise KeyError

    record.add_birthday(birthday)
    return birthday_added_message()
