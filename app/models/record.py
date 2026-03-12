"""Record class for storing contact information."""

from uuid import UUID, uuid4

from app.message_texts import PHONE_NOT_FOUND_IN_RECORD

from .address import Address
from .birthday import Birthday
from .email import Email
from .exceptions import PhoneNotFoundError
from .name import Name
from .phone import Phone


class Record:
    """Class for storing contact information including name, phones, and birthday."""

    def __init__(self, name: str) -> None:
        """Initialize record with contact name."""

        self.id: UUID = uuid4()
        self.name: Name = Name(name)
        self.phones: list[Phone] = []
        self.email: Email | None = None
        self.address: Address | None = None
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        """Add a phone number to the record."""

        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Remove a phone number from the record."""

        normalized = Phone.normalize(phone)
        self.phones = [p for p in self.phones if p.value != normalized]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Edit an existing phone number in the record."""

        normalized_old = Phone.normalize(old_phone)
        phone_found: bool = False

        for i, phone in enumerate(self.phones):
            if phone.value == normalized_old:
                self.phones[i] = Phone(new_phone)
                phone_found = True
                break

        if not phone_found:
            raise PhoneNotFoundError(PHONE_NOT_FOUND_IN_RECORD.format(phone=old_phone))

    def find_phone(self, phone: str) -> str | None:
        """Find and return a phone number if it exists in the record."""

        for p in self.phones:
            if p.value == phone:
                return p.value

        return None

    def add_birthday(self, birthday: str) -> None:
        """Add a birthday to the record."""

        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        """Add or update an email for the record."""

        self.email = Email(email)

    def add_address(self, address: str) -> None:
        """Add or update an address for the record."""

        self.address = Address(address)

    def __str__(self) -> str:
        """Return string representation of contact record."""

        phones_str = "; ".join(p.value for p in self.phones)
        result = f"Contact name: {self.name.value}, phones: {phones_str}"

        email = getattr(self, "email", None)
        if email:
            result += f", email: {email.value}"

        address = getattr(self, "address", None)
        if address:
            result += f", address: {address.value}"

        if self.birthday:
            result += f", birthday: {self.birthday.value}"

        return result
