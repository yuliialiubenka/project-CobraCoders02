from functools import wraps
from typing import Callable

from app.message_texts import (
    INPUT_ERROR_CONTACT_NOT_FOUND,
    INPUT_ERROR_ENTER_NAME,
    INPUT_ERROR_MISSING_ARGS,
    UNKNOWN_COMMAND,
)
from app.models.exceptions import RecordError


def _format_input_exception(exc: Exception) -> str:
    """Convert known input exceptions to user-friendly messages."""

    message = INPUT_ERROR_MISSING_ARGS

    if isinstance(exc, ValueError):
        if hasattr(exc, "custom_message"):
            message = exc.custom_message
    elif isinstance(exc, KeyError):
        if exc.args and exc.args[0] == "unknown_command":
            message = UNKNOWN_COMMAND
        else:
            message = INPUT_ERROR_CONTACT_NOT_FOUND
    elif isinstance(exc, IndexError):
        message = INPUT_ERROR_ENTER_NAME
    elif isinstance(exc, RecordError):
        message = str(exc)

    return message


def input_error(func: Callable[..., str]) -> Callable[..., str]:
    """
    Decorator to handle input errors in command handler functions.

    Catches common exceptions (ValueError, KeyError, IndexError, RecordError) and returns
    user-friendly error messages instead of letting the program crash.

    Args:
        func: Function to wrap with error handling.

    Returns:
        Wrapped function that handles exceptions gracefully.

    Example:
        >>> @input_error
        ... def add_contact(args, contacts):
        ...     name, phone = args
        ...     contacts[name] = phone
        ...     return "Contact added."
    """

    @wraps(func)
    def inner(*args: object, **kwargs: object) -> str:
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError, RecordError) as exc:
            return _format_input_exception(exc)

    return inner
