from functools import wraps
from typing import Callable

from app.message_texts import (
    INPUT_ERROR_CONTACT_NOT_FOUND,
    INPUT_ERROR_ENTER_NAME,
    INPUT_ERROR_MISSING_ARGS,
    UNKNOWN_COMMAND,
)


def input_error(func: Callable[..., str]) -> Callable[..., str]:
    """
    Decorator to handle input errors in command handler functions.

    Catches common exceptions (ValueError, KeyError, IndexError) and returns
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
        except ValueError as exc:
            if hasattr(exc, "custom_message"):
                return exc.custom_message
            return INPUT_ERROR_MISSING_ARGS
        except KeyError as exc:
            if exc.args and exc.args[0] == "unknown_command":
                return UNKNOWN_COMMAND
            return INPUT_ERROR_CONTACT_NOT_FOUND
        except IndexError:
            return INPUT_ERROR_ENTER_NAME

    return inner
