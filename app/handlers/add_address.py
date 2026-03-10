from app.decorators import colored_output, input_error
from app.messages import (
    address_saved_message,
    error_invalid_address_format,
    error_invalid_name_format,
    error_missing_args_add_address,
)
from app.models import AddressBook, Record
from app.validators import is_valid_address, is_valid_name


def _address_score(address_tokens: list[str]) -> int:
    """Score how likely tokens represent an address (higher is better)."""

    score = 0
    normalized_tokens = [token.strip(".,") for token in address_tokens]

    has_digit = any(any(char.isdigit() for char in token) for token in address_tokens)
    has_punctuation = any(
        any(char in ",./#-" for char in token) for token in address_tokens
    )

    if has_digit:
        score += 3
    if has_punctuation:
        score += 1
    if len(address_tokens) >= 2:
        score += 1
    if len(address_tokens) >= 3:
        score += 1

    if address_tokens and any(char.isdigit() for char in address_tokens[0]):
        score += 2

    if (
        len(address_tokens) >= 2
        and normalized_tokens[0].isalpha()
        and any(char.isdigit() for char in address_tokens[1])
    ):
        score += 2

    return score


def _split_name_and_address(args: list[str], book: AddressBook) -> tuple[str, str]:
    """Split command args into name and address without requiring quotes.

    Supports an optional '--' delimiter: add-address Name -- Address
    Falls back to heuristic scoring if no delimiter is present.
    """

    if len(args) < 2:
        error = ValueError(error_missing_args_add_address())
        error.custom_message = error_missing_args_add_address()
        raise error

    # Explicit '--' delimiter takes priority over heuristics.
    if "--" in args:
        sep_idx = args.index("--")
        name = " ".join(args[:sep_idx])
        address = " ".join(args[sep_idx + 1 :])
        return name, address

    # First, prefer the longest prefix that matches an existing contact name.
    for split_idx in range(len(args) - 1, 0, -1):
        candidate_name = " ".join(args[:split_idx])
        if book.find(candidate_name) is not None:
            return candidate_name, " ".join(args[split_idx:])

    # If contact is new, evaluate all valid splits and pick the most plausible address.
    candidates: list[tuple[int, int, str, str]] = []
    for split_idx in range(1, len(args)):
        candidate_name = " ".join(args[:split_idx])
        candidate_address = " ".join(args[split_idx:])

        if is_valid_name(candidate_name) and is_valid_address(candidate_address):
            score = _address_score(args[split_idx:])
            candidates.append((score, split_idx, candidate_name, candidate_address))

    if candidates:
        best_score = max(score for score, _, _, _ in candidates)
        best_candidates = [item for item in candidates if item[0] == best_score]

        # For ties, prefer longer name split to support multi-word names.
        _, _, name, address = max(best_candidates, key=lambda item: item[1])
        return name, address

    # Finally, fall back to 1-word name and the rest as address.
    return args[0], " ".join(args[1:])


@colored_output()
@input_error
def add_address(args: list[str], book: AddressBook) -> str:
    """Add or update an address for a contact."""

    name, address = _split_name_and_address(args, book)

    if not is_valid_name(name):
        return error_invalid_name_format()

    if not is_valid_address(address):
        return error_invalid_address_format()

    record = book.find(name)
    updated = False

    if record is None:
        record = Record(name)
        book.add_record(record)
    elif getattr(record, "address", None) is not None:
        updated = True

    record.add_address(address)
    return address_saved_message(updated)
