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
def search_contacts(args: list[str], book: AddressBook) -> str:
    """Search contacts by partial match across contact fields."""

    query = args[0]
    matching_records = book.search(query)

    if not matching_records:
        return no_matching_contacts_message()

    return format_contact_records(matching_records, title="=== Search Results ===")
