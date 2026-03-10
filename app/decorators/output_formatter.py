from functools import wraps
from typing import Callable

from colorama import Fore, Style


def output_formatter(
    color: str = Fore.WHITE,
    bold: bool = False,
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
            return f"{style}{color}{result}{Style.RESET_ALL}"

        return wrapper

    return decorator
