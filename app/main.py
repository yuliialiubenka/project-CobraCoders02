from colorama import init

from app.input_parser import parse_input
from app.handlers import execute_command
from app.messages import (
    welcome_message,
    goodbye_message,
    prompt_for_command,
)
from app.storage import load_data, save_data

# Initialize colorama for Windows compatibility
init(autoreset=True)


def main() -> None:
    """
    Main CLI loop for the contact assistant bot.

    Provides an interactive command-line interface for managing contacts.
    Supported commands:
    - hello: Display greeting
    - add <name> <phone>: Add a new contact
    - change <name> <old_phone> <new_phone>: Update phone number
    - add-email <name> <email>: Add or update contact email
    - add-address <name> <address>: Add or update contact address
    - phone <name>: Look up a contact's phone numbers
    - show-email <name>: Show email for a contact
    - show-address <name>: Show address for a contact
    - search <query>: Search contacts by any stored field
    - delete <name>: Remove a contact
    - all: Display all contacts in a formatted table
    - add-birthday <name> <date>: Add birthday (DD.MM.YYYY)
    - show-birthday <name>: Show birthday for a contact
    - birthdays [days]: Show upcoming birthdays (default: next 7 days)
    - close/exit: Terminate the program

    The bot runs in an infinite loop until the user enters "close" or "exit".
    """

    book = load_data()

    print(welcome_message())

    try:
        while True:
            user_input = input(prompt_for_command())

            # Skip empty input
            if not user_input.strip():
                continue

            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                print(goodbye_message())
                break

            result = execute_command(command, args, book)

            if result:  # Only print if there's a result
                print(result)

    except (KeyboardInterrupt, EOFError):
        print()
        print(goodbye_message())
    finally:
        save_data(book)


# For testing purposes
if __name__ == "__main__":
    main()
