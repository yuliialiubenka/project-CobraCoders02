from app.decorators import colored_output, input_error, validate_args
from app.messages import error_missing_args_search, no_matching_contacts_message
from app.models import AddressBook

from .show_all import format_contact_records


@colored_output()
@input_error
@validate_args(
    required_count=1,
    normalize_args=True,
    missing_args_message=error_missing_args_search(),
)


def search_name(args: list[str], book: AddressBook) -> str:
    """Search contacts by partial match across contact fields."""

    name = args[0]
    matching_records = book.search(name)

    if not matching_records:
        return no_matching_contacts_message()

    return format_contact_records(matching_records, title="=== Search Results ===")


def search_phone(args: list[str], book: AddressBook) -> str:
    """Search contacts by partial match across contact fields."""

    phone = args[0]
    matching_records = book.find_phone(phone)

    if not matching_records:
        return no_matching_contacts_message()

    return format_contact_records([matching_records], title="=== Search Results ===")


def search_email(args, book: AddressBook) -> str:
    """Search contacts by partial match across contact fields."""

    email = args[0]
    matching_records = book.find_email(email)

    if not matching_records:
        return no_matching_contacts_message()

    return format_contact_records([matching_records], title="=== Search Results ===")
 

def search_birthday(args, book: AddressBook) -> str:
    """Search contacts by match birthday fields."""

    birthday = args[0]
    matching_records = book.find_birthday(birthday)

    if not matching_records:
        return no_matching_contacts_message()

    return format_contact_records([matching_records], title="=== Search Results ===")
 