"""Command handlers package."""

from .add_address import add_address
from .add_birthday import add_birthday
from .add_contact import add_contact
from .add_email import add_email
from .birthdays import birthdays
from .change_contact import change_contact
from .delete_contact import delete_contact
from .execute_command import execute_command
from .show_all import show_all
from .show_address import show_address
from .show_birthday import show_birthday
from .show_email import show_email
from .show_phone import show_phone
from .delete_note import delete_note
from .edit_note import edit_note
from .search_notes import search_notes
from .show_notes import show_notes
from .search_contacts import search_name
from .search_contacts import search_phone
from .search_contacts import search_email
from .search_contacts import search_address
from .search_contacts import search_birthday

__all__ = [
    "add_address",
    "add_contact",
    "add_email",
    "change_contact",
    "show_phone",
    "show_all",
    "show_address",
    "delete_contact",
    "add_birthday",
    "show_birthday",
    "show_email",
    "birthdays",
    "delete_note",
    "edit_note",
    "search_notes",
    "show_notes",
    "execute_command",
    "search_name",
    "search_phone",
    "search_email",
    "search_address",
    "search_birthday",
]
