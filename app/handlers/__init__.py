"""Command handlers package."""

from .add_address import add_address
from .add_birthday import add_birthday
from .add_contact import add_contact
from .add_email import add_email
from .birthdays import birthdays
from .change_contact import change_contact
from .delete_contact import delete_contact
from .execute_command import execute_command
from .search_contacts import search_contacts
from .show_all import show_all
from .show_address import show_address
from .show_birthday import show_birthday
from .show_email import show_email
from .show_phone import show_phone

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
    "search_contacts",
    "birthdays",
    "execute_command",
]
