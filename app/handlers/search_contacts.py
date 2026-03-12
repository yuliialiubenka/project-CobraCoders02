import re

from app.decorators import colored_output, input_error, validate_args
from app.messages import error_missing_args_search, no_matching_contacts_message
from app.models import AddressBook, Record

from .show_all import format_contact_records


def _sorted(records: list[Record]) -> list[Record]:
    """Sort records by normalized contact name."""

    return sorted(records, key=lambda record: record.name.value.lower())


@colored_output()
@input_error
@validate_args(
    required_count=1,
    normalize_args=True,
    missing_args_message=error_missing_args_search(),
)
def search_contacts(args: list[str], book: AddressBook) -> str:
    """Search contacts across all available fields (partial match)."""

    query = args[0].strip().lower()
    query_digits = re.sub(r"\D", "", args[0])

    matches = []
    for record in book.data.values():
        in_name = query in record.name.value.lower()
        in_phone = bool(query_digits) and any(
            query_digits in phone.value for phone in record.phones
        )
        in_email = bool(getattr(record, "email", None)) and (
            query in record.email.value.lower()
        )
        in_address = bool(getattr(record, "address", None)) and (
            query in record.address.value.lower()
        )
        in_birthday = bool(getattr(record, "birthday", None)) and (
            query in record.birthday.value.lower()
        )

        if in_name or in_phone or in_email or in_address or in_birthday:
            matches.append(record)

    if not matches:
        return no_matching_contacts_message()

    return format_contact_records(_sorted(matches), title="=== Search Results ===")


@colored_output()
@input_error
@validate_args(
    required_count=1,
    normalize_args=True,
    missing_args_message=error_missing_args_search(),
)
def search_name(args: list[str], book: AddressBook) -> str:
    """Search contacts by name (partial, case-insensitive)."""

    query = args[0].strip().lower()
    matches = [
        record for record in book.data.values() if query in record.name.value.lower()
    ]

    if not matches:
        return no_matching_contacts_message()

    return format_contact_records(_sorted(matches), title="=== Search Name Results ===")


@colored_output()
@input_error
@validate_args(
    required_count=1,
    normalize_args=True,
    missing_args_message=error_missing_args_search(),
)
def search_phone(args: list[str], book: AddressBook) -> str:
    """Search contacts by phone (partial digits match)."""

    query_digits = re.sub(r"\D", "", args[0])
    if not query_digits:
        return no_matching_contacts_message()

    matches = [
        record
        for record in book.data.values()
        if any(query_digits in phone.value for phone in record.phones)
    ]

    if not matches:
        return no_matching_contacts_message()

    return format_contact_records(
        _sorted(matches), title="=== Search Phone Results ==="
    )


@colored_output()
@input_error
@validate_args(
    required_count=1,
    normalize_args=True,
    missing_args_message=error_missing_args_search(),
)
def search_email(args: list[str], book: AddressBook) -> str:
    """Search contacts by email (partial, case-insensitive)."""

    query = args[0].strip().lower()
    matches = [
        record
        for record in book.data.values()
        if getattr(record, "email", None) and query in record.email.value.lower()
    ]

    if not matches:
        return no_matching_contacts_message()

    return format_contact_records(
        _sorted(matches), title="=== Search Email Results ==="
    )


@colored_output()
@input_error
@validate_args(
    required_count=1,
    normalize_args=True,
    missing_args_message=error_missing_args_search(),
)
def search_address(args: list[str], book: AddressBook) -> str:
    """Search contacts by address (partial, case-insensitive)."""

    query = args[0].strip().lower()
    matches = [
        record
        for record in book.data.values()
        if getattr(record, "address", None) and query in record.address.value.lower()
    ]

    if not matches:
        return no_matching_contacts_message()

    return format_contact_records(
        _sorted(matches), title="=== Search Address Results ==="
    )


@colored_output()
@input_error
@validate_args(
    required_count=1,
    normalize_args=True,
    missing_args_message=error_missing_args_search(),
)
def search_birthday(args: list[str], book: AddressBook) -> str:
    """Search contacts by birthday (partial DD.MM.YYYY match)."""

    query = args[0].strip().lower()
    matches = [
        record
        for record in book.data.values()
        if getattr(record, "birthday", None) and query in record.birthday.value.lower()
    ]

    if not matches:
        return no_matching_contacts_message()

    return format_contact_records(
        _sorted(matches), title="=== Search Birthday Results ==="
    )
