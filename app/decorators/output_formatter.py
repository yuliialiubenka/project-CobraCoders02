from functools import wraps
from typing import Callable

from colorama import Fore, Style


def _is_structured_message(message: str) -> bool:
    """Return True for tabular or banner-like blocks that should stay unprefixed."""

    stripped_message = message.strip()
    if not stripped_message:
        return False

    lines = stripped_message.splitlines()

    if stripped_message.startswith("==="):
        return True

    if any(" | " in line for line in lines):
        return True

    return any(line and set(line) <= {"=", "-", "+"} for line in lines)


def output_formatter(
    color: str = Fore.WHITE,
    bold: bool = False,
    speaker: str | None = "COBRA",
) -> Callable[[Callable[..., str]], Callable[..., str]]:
    """
    Decorator to format function output with specific color and style.

    Applies a specific color and optionally bold style to the function's
    return value. Useful for consistently styling specific types of output.

    Args:
        color: Colorama color code to apply (default: Fore.WHITE).
        bold: Whether to make the text bold using Style.BRIGHT (default: False).

    Returns:
        Decorator function that wraps the target function.

    Example:
        >>> @output_formatter(color=Fore.CYAN, bold=True)
        ... def show_title():
        ...     return "=== Contact List ==="
        >>> show_title()  # Will print in bright cyan
        "=== Contact List ==="
    """

    def decorator(func: Callable[..., str]) -> Callable[..., str]:
        @wraps(func)
        def wrapper(*args: object, **kwargs: object) -> str:
            result = func(*args, **kwargs)
            style = Style.BRIGHT if bold else ""
            if speaker and not _is_structured_message(result):
                prefix = f"{Fore.CYAN}{style}{speaker}:{Style.RESET_ALL} "
                return prefix + f"{style}{color}{result}{Style.RESET_ALL}"
            return f"{style}{color}{result}{Style.RESET_ALL}"

        return wrapper

    return decorator
