from functools import wraps
from typing import Callable

from colorama import Fore, Style

from app.decorators.output_formatter import _is_structured_message


def colored_output(
    success_color: str = Fore.GREEN,
    error_color: str = Fore.RED,
    info_color: str = Fore.BLUE,
    speaker: str | None = "COBRA",
) -> Callable[[Callable[..., str]], Callable[..., str]]:
    """
    Decorator to apply colored formatting to function output.

    Automatically colors the output based on the content or result type.
    Success messages are displayed in green, error messages in red,
    and informational messages in blue by default.

    Args:
        success_color: Color for success messages (default: Fore.GREEN).
        error_color: Color for error messages (default: Fore.RED).
        info_color: Color for informational messages (default: Fore.BLUE).

    Returns:
        Decorator function that wraps the target function.

    Example:
        >>> @colored_output()
        ... def greet():
        ...     return "Hello!"
        >>> greet()  # Will print in green
        "Hello!"
    """

    def decorator(func: Callable[..., str]) -> Callable[..., str]:
        @wraps(func)
        def wrapper(*args: object, **kwargs: object) -> str:
            result = func(*args, **kwargs)

            if isinstance(result, str):
                if Style.RESET_ALL in result:
                    return result

                result_lower = result.lower()

                if any(
                    word in result_lower
                    for word in ["error", "not found", "invalid", "give me", "unknown"]
                ):
                    color = error_color
                elif any(
                    word in result_lower for word in ["added", "updated", "contact"]
                ):
                    color = success_color
                else:
                    color = info_color

                if speaker and not _is_structured_message(result):
                    prefix = f"{Fore.CYAN}{speaker}:{Style.RESET_ALL} "
                    return prefix + f"{color}{result}{Style.RESET_ALL}"
                return f"{color}{result}{Style.RESET_ALL}"

            color = info_color
            return f"{color}{result}{Style.RESET_ALL}"

        return wrapper

    return decorator
