"""AddressBook class for storing and managing contact records."""

from collections import UserDict
from datetime import datetime

from .record import Record


class AddressBook(UserDict):
    """Class for storing records and managing contacts."""

    def add_record(self, record: Record) -> None:
        """Add a record to the address book."""

        self.data[record.id] = record

    def find(self, name: str) -> Record | None:
        """Find a record by name."""

        for record in self.data.values():
            if record.name.value.lower() == name.lower():
                return record
        return None

    def delete(self, name: str) -> None:
        """Delete a record by name."""

        record = self.find(name)
        if record:
            del self.data[record.id]

    def search(self, query: str) -> list[Record]:
        """Search contacts by name, phone, email, address, or birthday."""

        normalized_query = query.strip().lower()
        if not normalized_query:
            return []

        matches: list[Record] = []

        for record in self.data.values():
            searchable_fields = [record.name.value]
            searchable_fields.extend(phone.value for phone in record.phones)

            email = getattr(record, "email", None)
            if email:
                searchable_fields.append(email.value)

            address = getattr(record, "address", None)
            if address:
                searchable_fields.append(address.value)

            if record.birthday:
                searchable_fields.append(record.birthday.value)

            haystack = " ".join(searchable_fields).lower()
            if normalized_query in haystack:
                matches.append(record)

        return sorted(matches, key=lambda record: record.name.value.lower())

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
