# COBRA — Contact Organizer & Basic Reminder Assistant

This project contains a CLI contact assistant bot with OOP address book models and persistent storage via pickle (load on start, save on exit).

## Quick Start

### 1. Create Virtual Environment

```cmd
python -m venv .venv
```

### 2. Activate Virtual Environment

**Windows (cmd or PowerShell):**

```cmd
.venv\Scripts\activate
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

### 4. Run the CLI Bot

```cmd
python -m app.main
```

```bash
python -m app.main
```

### 5. Run Tests

```cmd
python test_add_users.py
```

## Overview

### CLI Contact Assistant Bot

Interactive console application for contact management with input validation and error handling.

**Technologies:**

- Modular architecture (separate modules for handlers, validators, messages)
- Decorators for error handling and output formatting
- `colorama` for colored terminal messages
- Validation for names, phones, emails, and addresses
- Dictionary-based contact storage
- `pickle`-based persistence (`task/storage.py`)

**Available Commands:**

- `hello` — greeting
- `add <name> <phone>` — add contact with phone number (or add phone to existing contact)
- `change <name> <old_phone> <new_phone>` — change existing phone number
- `add-email <name> <email>` — add or update contact email
- `add-address <name> -- <address>` — add or update contact address (separator is required)
- `add-note <text>` — add a standalone note (max 50 characters; stored in notes.pkl)
- `phone <name>` — show phone numbers for contact
- `show-email <name>` — show email for contact
- `show-address <name>` — show address for contact
- `show-notes` — show all notes
- `search <query>` — search contacts by name, phone, email, address, or birthday
- `delete <name>` — delete contact from address book
- `add-birthday <name> <birthday>` — add birthday to contact (DD.MM.YYYY format)
- `show-birthday <name>` — show birthday for contact
- `birthdays [days]` — show contacts with upcoming birthdays (default: next 7 days)
- `all` — show all contacts with details
- `close` / `exit` — exit program

**Phone Format:**

- Accepts: `0501234567`, `050-123-4567`, `(050)123-4567`
- Must be 10 digits starting with 0
- No spaces or international prefix allowed

**Usage Examples:**

```cmd
python -m app.main

REM In interactive mode:
>>> add John 0501234567
>>> add-email John john@example.com
>>> add-address John -- 12 Main Street, Kyiv
>>> phone John
>>> change John 0501234567 0509876543
>>> search example.com
>>> birthdays 30
>>> all
>>> close
```

### Address Book Models

OOP-based address book implementation in `task/models/` package with proper encapsulation and validation.

**Architecture:**

- **Field** — base class for all fields
- **Name** — name field with validation (min 2 chars, letters only)
- **Phone** — phone field with validation and normalization
- **Email** — email field with validation and normalization
- **Address** — address field with basic validation
- **Record** — contact record managing name and multiple phones
- **AddressBook** — main container inheriting from `UserDict`
- **Custom Exceptions** — hierarchy for error handling

**Key Features:**

- ✅ Type hints throughout all code
- ✅ Custom exception hierarchy (`AddressBookError`, `FieldError`, `RecordError`)
- ✅ Phone normalization (flexible input → 10 digits storage)
- ✅ Name validation (letters, spaces, hyphens, apostrophes)
- ✅ Email validation and normalization to lowercase
- ✅ Address storage with basic validation
- ✅ Search across name, phone, email, address, and birthday
- ✅ Centralized error messages in constants
- ✅ Full inheritance chain (Field → Name/Phone)
- ✅ Persistent storage with `pickle` (`addressbook.pkl`)
- ✅ Safe startup fallback: if save file is missing/corrupted, app loads an empty address book

**Test File:**

Run [test_add_users.py](test_add_users.py) to validate core command flow:

```cmd
python test_add_users.py
```

## Project Structure

```
goit-pycore-hw-08/
├── task/
│   ├── handlers/               # Command handlers package
│   │   ├── __init__.py         # Package exports
│   │   ├── add_contact.py      # add command handler
│   │   ├── add_email.py        # add-email command handler
│   │   ├── add_address.py      # add-address command handler
│   │   ├── change_contact.py   # change command handler
│   │   ├── search_contacts.py  # search command handler
│   │   ├── show_phone.py       # phone command handler
│   │   ├── show_email.py       # show-email command handler
│   │   ├── show_address.py     # show-address command handler
│   │   ├── delete_contact.py   # delete command handler
│   │   ├── show_all.py         # all command handler
│   │   ├── add_birthday.py     # add-birthday command handler
│   │   ├── show_birthday.py    # show-birthday command handler
│   │   ├── birthdays.py        # birthdays command handler
│   │   └── execute_command.py  # Command dispatcher
│   ├── decorators/             # Decorators package
│   │   ├── __init__.py         # Package exports
│   │   ├── validate_args.py    # Argument validation decorator
│   │   ├── input_error.py      # Exception handling decorator
│   │   ├── colored_output.py   # Semantic color formatting decorator
│   │   └── output_formatter.py # Fixed style formatting decorator
│   ├── models/                 # Address book models package
│   │   ├── __init__.py         # Package exports
│   │   ├── address.py          # Address field with validation
│   │   ├── address_book.py     # AddressBook class
│   │   ├── email.py            # Email field with validation
│   │   ├── exceptions.py       # Custom exceptions hierarchy
│   │   ├── field.py            # Base Field class
│   │   ├── name.py             # Name field with validation
│   │   ├── phone.py            # Phone field with validation
│   │   ├── record.py           # Record class
│   │   └── birthday.py         # Birthday field with validation
│   ├── input_parser.py         # Command parsing logic
│   ├── main.py                 # CLI bot entry point
│   ├── message_texts.py        # Centralized message constants
│   ├── messages.py             # Message formatting utilities
│   ├── storage.py              # Pickle save/load helpers
│   └── validators.py           # Input validation functions
├── test_add_users.py           # Comprehensive integration test
├── requirements.txt            # Dependencies
└── README.md                   # Documentation
```

## Architecture & Design Patterns

### Modular Organization

- **handlers/** — Command implementation (each command in separate file)
- **decorators/** — Reusable decorators for validation, error handling, and formatting
- **models/** — Data structures with validation and business logic
- **validators.py** — Pure validation functions (reusable across CLI and models)
- **messages.py** — Formatted user-facing messages with colors
- **storage.py** — AddressBook persistence (load/save with pickle)
- **main.py** — CLI event loop

### Decorator Stack Pattern

Handlers use layered decorators for clean separation:

```python
@colored_output()           # Automatic color formatting (outer)
@input_error                # Exception → friendly message
@validate_args(...)         # Argument validation (inner)
def handler(args, book):
    pass
```

### Error Handling

- **Custom exceptions** in models layer for strict validation
- **Decorator-based** exception handling in CLI layer
- **Two-phase validation:** CLI validators → model validators

## Birthday Feature

Contacts can store birthdays in DD.MM.YYYY format:

```cmd
add-birthday John 25.12.1990
show-birthday John
birthdays 30                 # Show upcoming in the next 30 days
```

**Features:**

- Birthday validation with leap year support
- Upcoming birthday calculation window
- Birthday display integrated with contact list (`all` command)
- Independent birthday management (can be added/removed anytime)

## Technologies and Concepts

- **Python 3.12+** — modern version with type hints support
- **OOP** — inheritance (Field → Name/Phone), encapsulation, custom exceptions
- **Type Hints** — comprehensive type annotations (`str | None`, `list[Phone]`, etc.)
- **Custom Exceptions** — exception hierarchy for clear error handling
- **Decorators** — for error handling and output formatting
- **colorama** — colored terminal output
- **pickle** — serialization/deserialization for persistent storage
- **re (regular expressions)** — for validation and text parsing
- **shlex** — quote-aware CLI argument parsing
- **UserDict** — proper dictionary inheritance for AddressBook
- **Package Structure** — modular organization with `__init__.py` exports
- **Validation** — two-layer (CLI input + model level)
- **Data Normalization** — flexible phone input formats normalized to storage format

## Validation Rules

### Phone Numbers

- **Format:** Local 10-digit numbers only
- **Must start with:** 0
- **Accepted input:** `0501234567`, `050-123-4567`, `(050)123-4567`
- **Not allowed:** spaces, international prefix (`+380`)
- **Storage:** Normalized to 10 digits (`0501234567`)

### Names

- **Min length:** 2 characters
- **Allowed:** letters, spaces, hyphens, apostrophes
- **Not allowed:** numbers, special symbols
- **Examples:** `John`, `Mary-Jane`, `O'Brien`

### Emails

- **Format:** Standard email address (`local-part@domain`)
- **Examples:** `john@example.com`, `mary.jane@company.org`
- **Storage:** Normalized to lowercase

### Addresses

- **Min length:** 5 characters
- **Allowed:** letters, digits, spaces, commas, dots, slashes, hyphens, apostrophes, `#`
- **Required separator:** use `--` between name and address
- **Example:** `add-address John Smith -- 12 Main Street, Kyiv`

### Notes

- **Max length:** 50 characters (after trimming)
- **Empty:** Note text must be non-empty after stripping; otherwise validation fails
- **Storage:** Notes are stored in `notes.pkl` as a list of dicts with `id` (UUID4) and `text`; not tied to contacts
- **Commands:** `add-note <text>`, `show-notes`

## Requirements

See [requirements.txt](requirements.txt) for full dependency list.
