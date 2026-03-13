from typing import Callable
from functools import partial

from app.decorators import colored_output, input_error
from app.messages import error_unexpected_arguments, hello_message, help_message
from app.models import AddressBook, NotesBook

from .add_address import add_address
from .add_birthday import add_birthday
from .add_contact import add_contact
from .add_email import add_email
from .add_note import add_note
from .delete_note import delete_note
from .edit_note import edit_note
from .search_notes import search_notes
from .birthdays import birthdays
from .change_contact import change_contact
from .delete_contact import delete_contact
from .search_contacts import search_contacts
from .search_contacts import search_name
from .search_contacts import search_phone
from .search_contacts import search_email
from .search_contacts import search_address
from .search_contacts import search_birthday
from .show_all import show_all
from .show_address import show_address
from .show_birthday import show_birthday
from .show_email import show_email
from .show_notes import show_notes
from .show_phone import show_phone
from .search_tag import search_tag


@colored_output()
@input_error
def execute_command(
    command: str, args: list[str], book: AddressBook, notes_book: NotesBook
) -> str:
    """
    Execute a command by dispatching to appropriate handler.

    Args:
        command: Command name to execute.
        args: List of arguments for the command.
        book: AddressBook instance.
        notes_book: NotesBook instance.

    Returns:
        Result string from command execution.

    Raises:
        KeyError: If command is not recognized.
    """

    if not command:
        return ""

    commands: dict[str, tuple[Callable[..., str], str]] = {
        "hello": (hello_message, "none"),
        "help": (help_message, "none"),
        "add": (add_contact, "args_book"),
        "change": (change_contact, "args_book"),
        "phone": (show_phone, "args_book"),
        "all": (show_all, "book"),
        "delete": (delete_contact, "args_book"),
        "add-email": (add_email, "args_book"),
        "add-address": (add_address, "args_book"),
        "add-note": (add_note, "args_notes"),
        "delete-note": (delete_note, "args_notes"),
        "edit-note": (edit_note, "args_notes"),
        "search-notes": (search_notes, "args_notes"),
        "show-email": (show_email, "args_book"),
        "show-address": (show_address, "args_book"),
        "show-notes": (show_notes, "notes_optional"),
        "search": (search_contacts, "args_book"),
        "search-name": (search_name, "args_book"),
        "search-phone": (search_phone, "args_book"),
        "search-email": (search_email, "args_book"),
        "search-address": (search_address, "args_book"),
        "search-birthday": (search_birthday, "args_book"),
        "add-birthday": (add_birthday, "args_book"),
        "show-birthday": (show_birthday, "args_book"),
        "birthdays": (birthdays, "args_book"),
        "search-tag": (search_tag, "tag"),
    }

    if command in commands:
        handler, mode = commands[command]

        # Check for unexpected arguments in no-args modes
        if mode in ("none", "book", "notes") and args:
            return error_unexpected_arguments(command)

        # Optional-args modes (handler validates args)
        if mode == "notes_optional":
            return handler(notes_book, args)

        # Dynamic dispatch based on mode
        dispatch_map: dict[str, Callable[[], str]] = {
            "none": partial(handler),
            "book": partial(handler, book),
            "notes": partial(handler, notes_book),
            "args_book": partial(handler, args, book),
            "args_notes": partial(handler, args, notes_book),
        }

        if mode in dispatch_map:
            return dispatch_map[mode]()

    raise KeyError("unknown_command")
