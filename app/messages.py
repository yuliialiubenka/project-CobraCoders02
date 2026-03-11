"""
Messages module for the contact assistant bot.

This module provides user-friendly message functions with formatting:
- Greeting messages
- Error messages
- Command prompts
"""

from colorama import Fore

from app.decorators import output_formatter
from app.message_texts import (
    INVALID_NAME_FORMAT,
    INVALID_PHONE_FORMAT,
    INVALID_EMAIL_FORMAT,
    INVALID_ADDRESS_FORMAT,
    INVALID_BIRTHDAY_FORMAT,
    INVALID_DAYS_FORMAT,
    INVALID_NOTE_FORMAT,
    WELCOME_MESSAGE,
    HELLO_MESSAGE,
    GOODBYE_MESSAGE,
    ERROR_UNEXPECTED_ARGUMENTS,
    PROMPT_FOR_COMMAND,
    NO_CONTACTS_FOUND,
    NO_NOTES_FOUND,
    BIRTHDAY_ADDED,
    EMAIL_ADDED,
    EMAIL_UPDATED,
    ADDRESS_ADDED,
    ADDRESS_UPDATED,
    CONTACT_DELETED,
    NOTE_ADDED,
    NO_EMAIL_FOUND,
    NO_ADDRESS_FOUND,
    NO_MATCHING_CONTACTS,
    NO_UPCOMING_BIRTHDAYS,
    INPUT_ERROR_MISSING_ARGS_CHANGE,
    INPUT_ERROR_MISSING_ARGS_ADD_EMAIL,
    INPUT_ERROR_MISSING_ARGS_ADD_ADDRESS,
    INPUT_ERROR_MISSING_ARGS_DELETE,
    INPUT_ERROR_MISSING_ARGS_SEARCH,
    INPUT_ERROR_MISSING_ARGS_ADD_NOTE,
)


@output_formatter(color=Fore.CYAN, bold=True)
def welcome_message() -> str:
    """Return welcome message for the assistant bot."""
    return WELCOME_MESSAGE


@output_formatter(color=Fore.GREEN)
def hello_message() -> str:
    """Return greeting message."""
    return HELLO_MESSAGE


@output_formatter(color=Fore.CYAN)
def goodbye_message() -> str:
    """Return goodbye message."""
    return GOODBYE_MESSAGE


@output_formatter(color=Fore.RED)
def error_unexpected_arguments(command: str) -> str:
    """Return error message when a command receives unexpected arguments."""
    return ERROR_UNEXPECTED_ARGUMENTS.format(command=command)


@output_formatter(color=Fore.RED)
def error_invalid_name_format() -> str:
    """Return error message for invalid name format."""
    return INVALID_NAME_FORMAT


@output_formatter(color=Fore.RED)
def error_invalid_phone_format() -> str:
    """Return error message for invalid phone format."""
    return INVALID_PHONE_FORMAT


@output_formatter(color=Fore.RED)
def error_invalid_email_format() -> str:
    """Return error message for invalid email format."""
    return INVALID_EMAIL_FORMAT


@output_formatter(color=Fore.RED)
def error_invalid_address_format() -> str:
    """Return error message for invalid address format."""
    return INVALID_ADDRESS_FORMAT


@output_formatter(color=Fore.RED)
def error_missing_args_change() -> str:
    """Return error message for missing arguments in change command."""
    return INPUT_ERROR_MISSING_ARGS_CHANGE


@output_formatter(color=Fore.RED)
def error_missing_args_add_email() -> str:
    """Return error message for missing arguments in add-email command."""
    return INPUT_ERROR_MISSING_ARGS_ADD_EMAIL


@output_formatter(color=Fore.RED)
def error_missing_args_add_address() -> str:
    """Return error message for missing arguments in add-address command."""
    return INPUT_ERROR_MISSING_ARGS_ADD_ADDRESS


@output_formatter(color=Fore.RED)
def error_missing_args_delete() -> str:
    """Return error message for missing arguments in delete command."""
    return INPUT_ERROR_MISSING_ARGS_DELETE


@output_formatter(color=Fore.RED)
def error_missing_args_search() -> str:
    """Return error message for missing arguments in search command."""
    return INPUT_ERROR_MISSING_ARGS_SEARCH


@output_formatter(color=Fore.RED)
def error_missing_args_add_note() -> str:
    """Return error message for missing arguments in add-note command."""
    return INPUT_ERROR_MISSING_ARGS_ADD_NOTE


@output_formatter(color=Fore.RED)
def error_invalid_note_format() -> str:
    """Return error message for invalid note format (empty or over 50 characters)."""
    return INVALID_NOTE_FORMAT


@output_formatter(color=Fore.YELLOW)
def prompt_for_command() -> str:
    """Return prompt message for requesting a command."""
    return PROMPT_FOR_COMMAND


@output_formatter(color=Fore.BLUE)
def no_contacts_found_message() -> str:
    """Return message when there are no contacts."""
    return NO_CONTACTS_FOUND


@output_formatter(color=Fore.BLUE)
def no_notes_found_message() -> str:
    """Return message when there are no notes."""
    return NO_NOTES_FOUND


@output_formatter(color=Fore.RED)
def error_invalid_birthday_format() -> str:
    """Return error message for invalid birthday format."""
    return INVALID_BIRTHDAY_FORMAT


@output_formatter(color=Fore.RED)
def error_invalid_days_format() -> str:
    """Return error message for invalid birthdays days format."""
    return INVALID_DAYS_FORMAT


@output_formatter(color=Fore.GREEN)
def birthday_added_message() -> str:
    """Return success message when birthday is added."""
    return BIRTHDAY_ADDED


@output_formatter(color=Fore.GREEN)
def email_saved_message(updated: bool = False) -> str:
    """Return success message when an email is added or updated."""
    return EMAIL_UPDATED if updated else EMAIL_ADDED


@output_formatter(color=Fore.GREEN)
def address_saved_message(updated: bool = False) -> str:
    """Return success message when an address is added or updated."""
    return ADDRESS_UPDATED if updated else ADDRESS_ADDED


@output_formatter(color=Fore.GREEN)
def contact_deleted_message() -> str:
    """Return success message when contact is deleted."""
    return CONTACT_DELETED


@output_formatter(color=Fore.GREEN)
def note_added_message() -> str:
    """Return success message when a note is saved."""
    return NOTE_ADDED


@output_formatter(color=Fore.BLUE)
def no_email_found_message() -> str:
    """Return message when a contact has no email."""
    return NO_EMAIL_FOUND


@output_formatter(color=Fore.BLUE)
def no_address_found_message() -> str:
    """Return message when a contact has no address."""
    return NO_ADDRESS_FOUND


@output_formatter(color=Fore.BLUE)
def no_matching_contacts_message() -> str:
    """Return message when search returns no contacts."""
    return NO_MATCHING_CONTACTS


@output_formatter(color=Fore.BLUE)
def no_upcoming_birthdays_message(days: int = 7) -> str:
    """Return message when there are no upcoming birthdays."""
    return NO_UPCOMING_BIRTHDAYS.format(days=days)
