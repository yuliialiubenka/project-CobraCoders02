"""
Centralized user-facing text constants for the assistant bot.
"""

INPUT_ERROR_MISSING_ARGS = "Give me name and phone please."
INPUT_ERROR_MISSING_ARGS_CHANGE = (
    "To change a phone number, provide: name, old phone, new phone.\n"
    "Usage: change [name] [old phone] [new phone]"
)
INPUT_ERROR_MISSING_ARGS_ADD_EMAIL = (
    "To add an email, provide: name and email.\n" + "Usage: add-email [name] [email]"
)
INPUT_ERROR_MISSING_ARGS_ADD_ADDRESS = (
    "To add an address, provide: name and address.\n"
    "Usage: add-address [name] [address]"
)
INPUT_ERROR_MISSING_ARGS_DELETE = (
    "To delete a contact, provide: name. " + "Usage: delete [name]"
)
INPUT_ERROR_MISSING_ARGS_SEARCH = (
    "To search contacts, provide a query.\n" + "Usage: search [query]"
)
INPUT_ERROR_MISSING_ARGS_ADD_NOTE = (
    "To add a note, provide note text (max 50 characters).\n"
    "Usage: add-note [note text]"
)
INPUT_ERROR_CONTACT_NOT_FOUND = "Contact not found."
INPUT_ERROR_ENTER_NAME = "Enter user name."

UNKNOWN_COMMAND = (
    "Unknown command. Try: hello, add, change, phone, all, delete, "
    "add-email, add-address, add-note, show-email, show-address, show-notes, search, "
    "add-birthday, show-birthday, birthdays, close, exit"
)

WELCOME_MESSAGE = "Welcome to the assistant bot!"
HELLO_MESSAGE = "How can I help you?"
GOODBYE_MESSAGE = "Good bye!"

ERROR_UNEXPECTED_ARGUMENTS = "Error: The command '{command}' does not accept arguments."

# PROMPT_FOR_ARGUMENT = "Enter the {arg_description} for the command {command}: "
PROMPT_FOR_COMMAND = "Enter a command: "

NO_CONTACTS_FOUND = "No contacts found."
NO_NOTES_FOUND = "No notes found."

INVALID_NAME_FORMAT = (
    "Invalid name format. Use letters with optional spaces, hyphens, or apostrophes."
)
INVALID_PHONE_FORMAT = (
    "Invalid phone format. Use local number (10 digits, no spaces).\n"
    "Examples: 0501234567 | 050-123-4567 | (050)123-4567"
)
INVALID_EMAIL_FORMAT = (
    "Invalid email format. Use a valid email address like user@example.com"
)
INVALID_ADDRESS_FORMAT = (
    "Invalid address format. Use at least 5 characters.\n"
    "Allowed: letters, digits, spaces, commas, dots, slashes, hyphens, apostrophes, #"
)
INVALID_BIRTHDAY_FORMAT = "Invalid date format. Use DD.MM.YYYY"
INVALID_DAYS_FORMAT = (
    "Invalid days format. Use a non-negative integer. Example: birthdays 7"
)
INVALID_NOTE_FORMAT = "Note must be 1 to 50 characters."
INVALID_ARGUMENT_FORMAT = "Invalid format for argument {arg_index}."

PHONE_NOT_FOUND_IN_RECORD = "Phone number {phone} not found in record"

BIRTHDAY_ADDED = "Birthday added."
BIRTHDAY_DELETED = "Birthday removed."
CONTACT_DELETED = "Contact deleted."
EMAIL_ADDED = "Email added."
EMAIL_UPDATED = "Email updated."
ADDRESS_ADDED = "Address added."
ADDRESS_UPDATED = "Address updated."
NOTE_ADDED = "Note saved."
NO_EMAIL_FOUND = "Email not set."
NO_ADDRESS_FOUND = "Address not set."
NO_MATCHING_CONTACTS = "No matching contacts found."
NO_UPCOMING_BIRTHDAYS = "No upcoming birthdays in the next {days} days."
