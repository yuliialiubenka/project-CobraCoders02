"""Base Field class for record fields."""


# pylint: disable=too-few-public-methods
class Field:
    """Base class for record fields."""

    def __init__(self, value: str) -> None:
        """Initialize field with value."""

        self.value: str = value

    def __str__(self) -> str:
        """Return string representation of field value."""

        return str(self.value)
