"""AddressBook class for storing and managing contact records."""

from collections import UserDict
from datetime import datetime

from .record import Record


class AddressBook(UserDict):
    """Class for storing records and managing contacts."""

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Normalize user-entered contact name for reliable lookups."""

        return " ".join(word.title() for word in name.strip().split())

    def add_record(self, record: Record) -> None:
        """Add a record to the address book."""

        self.data[record.id] = record

    def find(self, name: str) -> Record | None:
        """Find a record by name."""

        normalized_name = self._normalize_name(name)

        for record in self.data.values():
            if record.name.value == normalized_name:
                return record
        return None

    def delete(self, name: str) -> None:
        """Delete a record by name."""

        record = self.find(name)
        if record:
            del self.data[record.id]

    def get_upcoming_birthdays(self, days_ahead: int = 7) -> list[dict[str, str]]:
        """
        Get a list of contacts whose birthdays occur in the next given number of days.

        Returns:
            List of dicts with 'name' and 'birthday' keys for upcoming birthdays.
            If no upcoming birthdays, returns empty list.
        """
        today = datetime.today().date()
        upcoming: list[dict[str, str]] = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            # Get birthday date for this year
            birthday_date = record.birthday.date.date()
            birthday_this_year = birthday_date.replace(year=today.year)

            # If birthday already passed this year, check next year
            if birthday_this_year < today:
                birthday_this_year = birthday_date.replace(year=today.year + 1)

            # Check if birthday is within the requested range
            days_until_birthday = (birthday_this_year - today).days

            if 0 <= days_until_birthday <= days_ahead:
                upcoming.append(
                    {
                        "name": record.name.value,
                        "birthday": birthday_this_year.strftime("%d.%m.%Y"),
                    }
                )

        return upcoming
