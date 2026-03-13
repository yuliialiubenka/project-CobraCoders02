"""
Validators module for the contact assistant bot.

This module provides validation functions for different argument types:
- Phone number validation
- Name validation
- General format validators
"""

import re


def is_valid_phone(phone: str) -> bool:
    """
    Validate phone number format.

    Accepts local numbers only (10 digits starting with 0).
    Allows hyphens and parentheses as separators, but no spaces or '+'.

    Args:
        phone: Phone number string without spaces.

    Returns:
        True if phone number is valid, False otherwise.

    Example:
        >>> is_valid_phone("0987654321")
        True
        >>> is_valid_phone("098-765-4321")
        True
        >>> is_valid_phone("+380987654321")  # International is invalid here
        False
        >>> is_valid_phone("098 765-4321")  # Spaces NOT allowed
        False
    """

    if not isinstance(phone, str) or " " in phone:  # Reject if spaces present
        return False

    # Extract only digits
    digits_only = re.sub(r"\D", "", phone)

    # Local format: exactly 10 digits starting with 0, NO '+' allowed
    return len(digits_only) == 10 and digits_only.startswith("0") and "+" not in phone


def is_valid_email(email: str) -> bool:
    """
    Validate email format.

    Accepts standard local-part@domain email addresses.
    """

    if not isinstance(email, str):
        return False

    trimmed = email.strip()
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return bool(re.fullmatch(pattern, trimmed))


def is_valid_address(address: str) -> bool:
    """
    Validate address format.

    Requires at least 5 visible characters and allows common address punctuation.
    """

    if not isinstance(address, str):
        return False

    trimmed = address.strip()

    if len(trimmed) < 5:
        return False

    allowed_symbols = " .,/#-'"

    if not all(char.isalnum() or char in allowed_symbols for char in trimmed):
        return False

    return any(char.isalnum() for char in trimmed)


def is_valid_note_title(title: str) -> bool:
    """Validate note title format."""

    if not isinstance(title, str):
        return False

    trimmed = title.strip()
    return 0 < len(trimmed) <= 50


def is_valid_note_text(note_text: str) -> bool:
    """Validate note text format."""

    if not isinstance(note_text, str):
        return False

    trimmed = note_text.strip()
    return 0 < len(trimmed) <= 500


def is_valid_note_tag(tag: str) -> bool:
    """Validate a single note tag."""

    if not isinstance(tag, str):
        return False

    trimmed = tag.strip()
    return 0 < len(trimmed) <= 30 and "--" not in trimmed


def is_valid_name(name: str) -> bool:
    """
    Validate contact name format.

    Checks if name contains only letters, spaces, hyphens, and apostrophes.
    No leading/trailing separators and no consecutive separators.
    Minimum length: 2 characters.

    Args:
        name: Name string to validate.

    Returns:
        True if name is valid, False otherwise.

    Example:
        >>> is_valid_name("John")
        True
        >>> is_valid_name("Mary-Jane")
        True
        >>> is_valid_name("O'Brien")
        True
        >>> is_valid_name("123")
        False
    """

    trimmed = name.strip()

    if len(trimmed) < 2:
        return False

    # Allow letters, spaces, hyphens, and apostrophes only
    if not all(c.isalpha() or c in " -'" for c in trimmed):
        return False

    # Reject leading/trailing separators
    if trimmed[0] in " -'" or trimmed[-1] in " -'":
        return False

    # Reject consecutive separators (e.g., double spaces or "--")
    separators = " -'"
    prev_is_sep = False

    for char in trimmed:
        is_sep = char in separators

        if prev_is_sep and is_sep:
            return False

        prev_is_sep = is_sep

    return True


def is_valid_birthday(birthday: str) -> bool:
    """
    Validate birthday date format.

    Accepts dates in DD.MM.YYYY format.

    Args:
        birthday: Birthday string to validate.

    Returns:
        True if birthday format is valid, False otherwise.

    Example:
        >>> is_valid_birthday("25.12.1990")
        True
        >>> is_valid_birthday("31.02.2000")  # Invalid day for February
        False
        >>> is_valid_birthday("25/12/1990")  # Wrong separator
        False
    """

    if not isinstance(birthday, str):
        return False

    # Regular expression for DD.MM.YYYY format:
    # ^        - start of string (must begin here)
    # \d{2}    - exactly 2 digits (day)
    # \.       - literal dot (escaped \ to treat as literal character, not regex special char)
    # \d{2}    - exactly 2 digits (month)
    # \.       - literal dot (escaped)
    # \d{4}    - exactly 4 digits (year)
    # $        - end of string (must end here)
    # Valid examples: 25.12.1990, 01.03.2000
    # Invalid examples: 25/12/1990 (wrong separators), 25-12-1990, 5.3.2000 (too few digits)
    pattern = r"^\d{2}\.\d{2}\.\d{4}$"

    if not re.match(pattern, birthday):
        return False

    # Parse and validate date
    parts = birthday.split(".")
    day, month, year = int(parts[0]), int(parts[1]), int(parts[2])

    # Validate month
    if month < 1 or month > 12:
        return False

    # Days in each month
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Check for leap year
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    if is_leap:
        days_in_month[1] = 29

    # Validate day
    if day < 1 or day > days_in_month[month - 1]:
        return False

    return True

def is_valid_tag(tag: str) -> bool:
    """
    Validate tag format.

    Accepts standard #some_text&simbol_without_spase.
    """

    if not isinstance(tag, str):
        return False

    trimmed = tag.strip()
    pattern = r"#[^\s]+"

    return bool(re.fullmatch(pattern, trimmed))