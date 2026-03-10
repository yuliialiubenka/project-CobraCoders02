from app.decorators import colored_output, input_error, validate_args
from app.messages import error_invalid_name_format, no_email_found_message
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
def show_email(args: list[str], book: AddressBook) -> str:
    """Retrieve and return email for a specific contact."""

    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError

    email = getattr(record, "email", None)
    if email is None:
        return no_email_found_message()

    return f"{name}: {email.value}"
