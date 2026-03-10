from app.decorators import colored_output, input_error, validate_args
from app.messages import (
    email_saved_message,
    error_invalid_email_format,
    error_invalid_name_format,
    error_missing_args_add_email,
)
from app.models import AddressBook, Record
from app.validators import is_valid_email, is_valid_name


@colored_output()
@input_error
@validate_args(
    required_count=2,
    validators={0: is_valid_name, 1: is_valid_email},
    error_messages={
        0: error_invalid_name_format(),
        1: error_invalid_email_format(),
    },
    normalize_args=True,
    missing_args_message=error_missing_args_add_email(),
)
def add_email(args: list[str], book: AddressBook) -> str:
    """Add or update an email for a contact."""

    name, email = args
    record = book.find(name)
    updated = False

    if record is None:
        record = Record(name)
        book.add_record(record)
    elif getattr(record, "email", None) is not None:
        updated = True

    record.add_email(email)
    return email_saved_message(updated)
