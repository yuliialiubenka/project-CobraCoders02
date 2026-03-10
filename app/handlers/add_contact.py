from app.decorators import colored_output, input_error, validate_args
from app.messages import error_invalid_name_format, error_invalid_phone_format
from app.models import AddressBook, Record
from app.validators import is_valid_name, is_valid_phone


@colored_output()
@input_error
@validate_args(
    required_count=2,
    validators={0: is_valid_name, 1: is_valid_phone},
    error_messages={
        0: error_invalid_name_format(),
        1: error_invalid_phone_format(),
    },
    normalize_args=True,
)
def add_contact(args: list[str], book: AddressBook) -> str:
    """
    Add a new contact or phone number to an existing contact.

    Creates a new contact entry with the provided name and phone number.
    If a contact with the same name exists, adds the phone to that contact.

    Args:
        args: List of arguments where args[0] is contact name and args[1] is phone.
              Must contain at least 2 elements.
        book: AddressBook instance to store contact information.

    Returns:
        "Contact added." if new contact was created.
        "Contact updated." if phone was added to existing contact.

    Raises:
        ValueError: If insufficient arguments are provided (less than 2).

    Example:
        >>> book = AddressBook()
        >>> add_contact(["John", "0987654321"], book)
        "Contact added."
    """

    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    record.add_phone(phone)
    return message
