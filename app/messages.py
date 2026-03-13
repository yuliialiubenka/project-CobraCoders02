"""
Messages module for the contact assistant bot.

This module provides user-friendly message functions with formatting:
- Greeting messages
- Error messages
- Command prompts
"""

from difflib import get_close_matches

from colorama import Fore

from app.decorators import output_formatter
from app.message_texts import (
    INVALID_NAME_FORMAT,
    INVALID_PHONE_FORMAT,
    INVALID_EMAIL_FORMAT,
    INVALID_ADDRESS_FORMAT,
    INVALID_BIRTHDAY_FORMAT,
    INVALID_DAYS_FORMAT,
    INVALID_NOTE_TAGS_FORMAT,
    INVALID_NOTE_TEXT_FORMAT,
    INVALID_NOTE_TITLE_FORMAT,
    WELCOME_MESSAGE,
    STARTUP_GREETING_MESSAGE,
    HELLO_MESSAGE,
    GOODBYE_MESSAGE,
    ERROR_UNEXPECTED_ARGUMENTS,
    UNKNOWN_COMMAND,
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
    INPUT_ERROR_MISSING_ARGS_PHONE,
    INPUT_ERROR_MISSING_ARGS_CHANGE,
    INPUT_ERROR_MISSING_ARGS_ADD_EMAIL,
    INPUT_ERROR_MISSING_ARGS_ADD_ADDRESS,
    INPUT_ERROR_MISSING_DELIMITER_ADD_ADDRESS,
    INPUT_ERROR_MISSING_ARGS_DELETE,
    INPUT_ERROR_MISSING_ARGS_SEARCH,
    INPUT_ERROR_MISSING_ARGS_ADD_NOTE,
    INPUT_ERROR_MISSING_DELIMITER_ADD_NOTE,
    INPUT_ERROR_INVALID_DELIMITERS_ADD_NOTE,
    INPUT_ERROR_MISSING_ARGS_DELETE_NOTE,
    INPUT_ERROR_MISSING_ARGS_SEARCH_NOTES,
    INPUT_ERROR_MISSING_ARGS_EDIT_NOTE,
    INPUT_ERROR_MISSING_DELIMITER_EDIT_NOTE,
    INPUT_ERROR_INVALID_DELIMITERS_EDIT_NOTE,
    NOTE_DELETED,
    NOTE_DUPLICATE_TITLE,
    NOTE_UPDATED,
    NOTE_NOT_FOUND,
    NO_MATCHING_NOTES,
    HELP_COMMANDS,
)


@output_formatter(color=Fore.CYAN, bold=True, speaker=None)
def welcome_message() -> str:
    """Return welcome message for the assistant bot."""
    return WELCOME_MESSAGE


@output_formatter(color=Fore.CYAN)
def startup_greeting_message() -> str:
    """Return startup greeting shown after the welcome banner."""
    return STARTUP_GREETING_MESSAGE


@output_formatter(color=Fore.CYAN)
def hello_message() -> str:
    """Return greeting message."""
    return HELLO_MESSAGE


@output_formatter(color=Fore.CYAN, speaker=None)
def help_message() -> str:
    """Return help as a two-column aligned table matching the contacts style."""
    title = "=== Available Commands ==="
    col1_width = max(len(cmd) for cmd, _ in HELP_COMMANDS)
    col2_width = max(len(desc) for _, desc in HELP_COMMANDS)
    header = f"{'Command':<{col1_width}} | Description"
    divider = "-" * (col1_width + 1) + "+" + "-" * (col2_width + 1)
    rows = [f"{cmd:<{col1_width}} | {desc}" for cmd, desc in HELP_COMMANDS]
    separator = " " * len(title)
    return f"{title}\n{separator}\n{header}\n{divider}\n" + "\n".join(rows)


def _help_command_aliases() -> list[str]:
    """Build a normalized list of command aliases from HELP_COMMANDS."""

    aliases: list[str] = []

    for command_usage, _ in HELP_COMMANDS:
        if " / " in command_usage:
            aliases.extend(part.strip().lower() for part in command_usage.split("/"))
        else:
            aliases.append(command_usage.split()[0].strip().lower())

    # Preserve order and remove duplicates.
    return list(dict.fromkeys(aliases))


def unknown_command_message(command: str) -> str:
    """Return unknown-command message with the closest command suggestion."""

    normalized_command = command.strip().lower()

    if not normalized_command:
        return UNKNOWN_COMMAND

    suggestion = get_close_matches(
        normalized_command,
        _help_command_aliases(),
        n=1,
        cutoff=0.6,
    )

    if suggestion:
        return f"Unknown command. Try to use: {suggestion[0]}"

    return UNKNOWN_COMMAND


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
def error_missing_args_phone() -> str:
    """Return error message for missing arguments in phone command."""
    return INPUT_ERROR_MISSING_ARGS_PHONE


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
def error_missing_delimiter_add_address() -> str:
    """Return error message for missing '--' delimiter in add-address command."""
    return INPUT_ERROR_MISSING_DELIMITER_ADD_ADDRESS


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
def error_missing_delimiter_add_note() -> str:
    """Return error message for missing '--' delimiter in add-note command."""
    return INPUT_ERROR_MISSING_DELIMITER_ADD_NOTE


@output_formatter(color=Fore.RED)
def error_invalid_delimiters_add_note() -> str:
    """Return error message for too many '--' delimiters in add-note command."""
    return INPUT_ERROR_INVALID_DELIMITERS_ADD_NOTE


@output_formatter(color=Fore.RED)
def error_invalid_note_title_format() -> str:
    """Return error message for invalid note title format."""
    return INVALID_NOTE_TITLE_FORMAT


@output_formatter(color=Fore.RED)
def error_invalid_note_text_format() -> str:
    """Return error message for invalid note text format."""
    return INVALID_NOTE_TEXT_FORMAT


@output_formatter(color=Fore.RED)
def error_invalid_note_tags_format() -> str:
    """Return error message for invalid note tags format."""
    return INVALID_NOTE_TAGS_FORMAT


@output_formatter(color=Fore.YELLOW, speaker=None)
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


@output_formatter(color=Fore.RED)
def error_duplicate_note_title(title: str) -> str:
    """Return error message when a note with given title already exists."""
    return NOTE_DUPLICATE_TITLE.format(title=title)


@output_formatter(color=Fore.GREEN)
def note_deleted_message() -> str:
    """Return success message when a note is deleted."""
    return NOTE_DELETED


@output_formatter(color=Fore.BLUE)
def note_not_found_message() -> str:
    """Return message when a note is not found by title."""
    return NOTE_NOT_FOUND


@output_formatter(color=Fore.BLUE)
def no_matching_notes_message() -> str:
    """Return message when note search returns no results."""
    return NO_MATCHING_NOTES


@output_formatter(color=Fore.RED)
def error_missing_args_delete_note() -> str:
    """Return error message for missing arguments in delete-note command."""
    return INPUT_ERROR_MISSING_ARGS_DELETE_NOTE


@output_formatter(color=Fore.RED)
def error_missing_args_search_notes() -> str:
    """Return error message for missing arguments in search-notes command."""
    return INPUT_ERROR_MISSING_ARGS_SEARCH_NOTES


@output_formatter(color=Fore.RED)
def error_missing_args_edit_note() -> str:
    """Return error message for missing arguments in edit-note command."""
    return INPUT_ERROR_MISSING_ARGS_EDIT_NOTE


@output_formatter(color=Fore.RED)
def error_missing_delimiter_edit_note() -> str:
    """Return error message for missing '--' delimiter in edit-note command."""
    return INPUT_ERROR_MISSING_DELIMITER_EDIT_NOTE


@output_formatter(color=Fore.RED)
def error_invalid_delimiters_edit_note() -> str:
    """Return error message for invalid '--' delimiters in edit-note command."""
    return INPUT_ERROR_INVALID_DELIMITERS_EDIT_NOTE


@output_formatter(color=Fore.GREEN)
def note_updated_message() -> str:
    """Return success message when a note is updated."""
    return NOTE_UPDATED


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
