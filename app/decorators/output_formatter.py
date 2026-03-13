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


def _apply_speaker_prefix(message: str, speaker: str | None) -> str:
    """Prefix regular bot messages while leaving structured blocks untouched."""

    if not speaker or _is_structured_message(message):
        return message

    lines = message.splitlines()
    if not lines:
        return message

    lines[0] = f"{speaker}: {lines[0]}"
    return "\n".join(lines)


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
            formatted_result = _apply_speaker_prefix(result, speaker)
            return f"{style}{color}{formatted_result}{Style.RESET_ALL}"

        return wrapper

    return decorator
