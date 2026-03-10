from colorama import Fore

from app.decorators import colored_output, input_error
from app.messages import no_contacts_found_message
from app.models import AddressBook, Record


def format_contact_records(
    records: list[Record],
    title: str = "=== Contact List ===",
) -> str:
    """Format contact records as a vertical table."""

    if not records:
        return no_contacts_found_message()

    all_labels = ["Name", "Phones", "Email", "Address", "Birthday"]
    global_col1_width = max(len(label) for label in all_labels)

    all_tables = []

    for record in records:
        rows = [("Name", record.name.value)]

        phones_str = (
            ", ".join(phone.value for phone in record.phones) if record.phones else ""
        )
        if phones_str:
            rows.append(("Phones", phones_str))

        email = getattr(record, "email", None)
        if email:
            rows.append(("Email", email.value))

        address = getattr(record, "address", None)
        if address:
            rows.append(("Address", address.value))

        if record.birthday:
            rows.append(("Birthday", record.birthday.value))

        col2_width = max(len(value) for _, value in rows)
        table_lines = [
            f"{label:<{global_col1_width}} | {value:<{col2_width}}"
            for label, value in rows
        ]
        all_tables.append("\n".join(table_lines))

    separator = " " * len(title)
    return f"{title}\n{separator}\n" + "\n\n".join(all_tables)


@colored_output(success_color=Fore.BLUE, info_color=Fore.BLUE)
@input_error
def show_all(book: AddressBook) -> str:
    """
    Display all contacts in a formatted vertical table.

    Returns all contacts sorted alphabetically by name with complete information
    displayed in a vertical table format. Only displays fields that contain data.

    Args:
        book: AddressBook instance containing contact records.

    Returns:
        Formatted vertical table string with contact entries.
        Each contact displayed as a mini-table with aligned columns.
        Returns "No contacts found." if the address book is empty.

    Example:
        >>> book = AddressBook()
        >>> record = Record("John")
        >>> record.add_phone("0987654321")
        >>> book.add_record(record)
        >>> print(show_all(book))
        === Contact List ===
        Name    | John
        Phones  | 0987654321
    """

    sorted_records = sorted(
        book.data.values(), key=lambda record: record.name.value.lower()
    )
    return format_contact_records(sorted_records)
