import shlex


def parse_input(user_input: str) -> tuple[str, list[str]]:
    """
    Parse user input into a command and its arguments.

    Extracts the first word as the command (converted to lowercase) and
    remaining words as arguments.

    Args:
        user_input: Raw input string from user. If empty, returns empty command and args.

    Returns:
        Tuple of (command, arguments_list). Returns ("", []) if input is empty or None.

    Example:
        >>> parse_input("add John 0987654321")
        ("add", ["John", "0987654321"])
        >>> parse_input("")
        ("", [])
    """

    if not user_input or not user_input.strip():
        return "", []

    try:
        parts = shlex.split(user_input)
    except ValueError:
        parts = user_input.split()

    cmd, *args = parts

    return cmd.strip().lower(), args
