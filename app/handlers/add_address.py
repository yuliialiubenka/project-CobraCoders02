from app.decorators import colored_output, input_error
from app.messages import (
    address_saved_message,
    error_invalid_address_format,
    error_invalid_name_format,
    error_missing_delimiter_add_address,
    error_missing_args_add_address,
)
from app.models import AddressBook, Record
from app.validators import is_valid_address, is_valid_name


def _split_name_and_address(args: list[str]) -> tuple[str, str]:
    """Split args into name and address using mandatory '--' delimiter."""

    if len(args) < 2:
        error = ValueError(error_missing_args_add_address())
        error.custom_message = error_missing_args_add_address()

        raise error

    if "--" not in args:
        error = ValueError(error_missing_delimiter_add_address())
        error.custom_message = str(error)

        raise error

    sep_idx = args.index("--")
    name = " ".join(args[:sep_idx])
    address = " ".join(args[sep_idx + 1 :])

    if not name.strip() or not address.strip():
        error = ValueError(error_missing_args_add_address())
        error.custom_message = error_missing_args_add_address()

        raise error

    return name, address


@colored_output()
@input_error
def add_address(args: list[str], book: AddressBook) -> str:
    """Add or update an address for a contact."""

    name, address = _split_name_and_address(args)

    if not is_valid_name(name):
        return error_invalid_name_format()

    if not is_valid_address(address):
        return error_invalid_address_format()

    record = book.find(name)
    updated = False

    if record is None:
        record = Record(name)
        book.add_record(record)
    elif getattr(record, "address", None) is not None:
        updated = True

    record.add_address(address)

    return address_saved_message(updated)
