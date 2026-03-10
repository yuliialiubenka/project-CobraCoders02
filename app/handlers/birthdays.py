from app.decorators import colored_output, input_error
from app.messages import error_invalid_days_format, no_upcoming_birthdays_message
from app.models import AddressBook


@colored_output()
@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    """
    Show all upcoming birthdays in the next given number of days.

    Args:
        args: Optional list with one integer argument for days ahead.
        book: AddressBook instance.

    Returns:
        Formatted list of upcoming birthdays or message if none found.

    Example:
        >>> book = AddressBook()
        >>> birthdays([], book)
        "No upcoming birthdays in the next 7 days."
    """

    days_ahead = 7
    if args:
        if len(args) != 1 or not args[0].isdigit():
            return error_invalid_days_format()

        days_ahead = int(args[0])

    upcoming = book.get_upcoming_birthdays(days_ahead)

    if not upcoming:
        return no_upcoming_birthdays_message(days_ahead)

    lines = [f"{record['name']}: {record['birthday']}" for record in upcoming]
    return "\n".join(lines)
