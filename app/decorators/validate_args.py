from functools import wraps
from typing import Callable, Optional

from app.message_texts import INVALID_ARGUMENT_FORMAT


def validate_args(
    required_count: int,
    validators: Optional[dict[int, Callable[[str], bool]]] = None,
    error_messages: Optional[dict[int, str]] = None,
    normalize_args: bool = False,
    missing_args_message: Optional[str] = None,
) -> Callable[[Callable[..., str]], Callable[..., str]]:
    """
    Decorator to validate command arguments before execution.

    Validates both the number and format of arguments. Can check if arguments
    match expected patterns (e.g., phone numbers contain only digits).

    Args:
        required_count: Minimum number of arguments required.
        validators: Optional dict mapping argument index to validation function.
                   Example: {1: lambda x: x.isdigit()} to check if arg[1] is numeric.
        error_messages: Optional dict mapping argument index to custom error messages.
        normalize_args: When True, combines multi-word name arguments into a single value.
        missing_args_message: Custom message for missing arguments. If None, uses default.

    Returns:
        Decorator function that validates arguments before calling handler.

    Example:
        >>> @validate_args(
        ...     required_count=2,
        ...     validators={1: lambda x: x.isdigit()},
        ...     error_messages={1: "Phone number must contain only digits"}
        ... )
        ... def add_contact(args, contacts):
        ...     name, phone = args
        ...     contacts[name] = phone
        ...     return "Contact added."
    """

    def decorator(func: Callable[..., str]) -> Callable[..., str]:
        @wraps(func)
        def wrapper(args: list[str], *other_args: object, **kwargs: object) -> str:
            normalized_args = args
            if normalize_args:
                if required_count == 1 and len(args) > 1:
                    normalized_args = [" ".join(args)]
                elif required_count == 2 and len(args) > 2:
                    normalized_args = [" ".join(args[:-1]), args[-1]]
                elif required_count == 3 and len(args) > 3:
                    normalized_args = [" ".join(args[:-2]), args[-2], args[-1]]

            # Check if we have enough arguments
            if len(normalized_args) < required_count:
                if missing_args_message:
                    error = ValueError(missing_args_message)
                    error.custom_message = missing_args_message
                    raise error
                raise ValueError

            if validators:
                for idx, validator in validators.items():
                    if idx < len(normalized_args) and not validator(
                        normalized_args[idx]
                    ):
                        if error_messages and idx in error_messages:
                            return error_messages[idx]
                        return INVALID_ARGUMENT_FORMAT.format(arg_index=idx + 1)

            return func(normalized_args, *other_args, **kwargs)

        return wrapper

    return decorator
