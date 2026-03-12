"""Custom exceptions for address book models."""


class AddressBookError(Exception):
    """Base exception for address book operations."""

    def __init__(self, message: str) -> None:
        """Initialize exception with message."""

        super().__init__(message)
        self.message = message


class FieldError(AddressBookError):
    """Base exception for field validation errors."""


class InvalidNameError(FieldError):
    """Raised when name validation fails."""


class InvalidPhoneError(FieldError):
    """Raised when phone validation fails."""


class InvalidEmailError(FieldError):
    """Raised when email validation fails."""


class InvalidAddressError(FieldError):
    """Raised when address validation fails."""


class InvalidBirthdayError(FieldError):
    """Raised when birthday validation fails."""


class InvalidNoteError(FieldError):
    """Raised when note validation fails."""


class RecordError(AddressBookError):
    """Base exception for record operations."""


class PhoneNotFoundError(RecordError):
    """Raised when a phone number is not found in a record."""