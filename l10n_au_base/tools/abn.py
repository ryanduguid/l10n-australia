# Copyright 2026 Ryan Duguid
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Australian Business Number checksum and display format.

The weights and the 'subtract 1 from the first digit' step are the ABR
published algorithm:
https://abr.business.gov.au/Help/AbnFormat

This module does not call ABR or ATO services. A passing checksum is not
proof that the number is registered, and it is not lodgment advice.
"""

from __future__ import annotations

_WEIGHTS = (10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19)


def compact_abn(value: str | None) -> str:
    """Return the 11-digit ABN, or '' if value is empty.

    Accepts spaces and an optional AU prefix. Raises ValueError when the
    remaining characters are not exactly 11 digits.
    """
    if value is None:
        return ""
    text = "".join(ch for ch in str(value).upper() if ch.isalnum())
    if not text:
        return ""
    text = text.removeprefix("AU")
    # isdigit() alone accepts superscript and circled digits, which int()
    # then rejects. An ABN is 11 ASCII digits, so a pasted "5182475355²"
    # is invalid input rather than a number to convert.
    if len(text) != 11 or not (text.isascii() and text.isdigit()):
        raise ValueError("ABN must be 11 digits (optional AU prefix and spaces).")
    return text


def format_abn(value: str | None) -> str:
    """Return 'NN NNN NNN NNN', or '' if value is empty."""
    digits = compact_abn(value)
    if not digits:
        return ""
    return f"{digits[:2]} {digits[2:5]} {digits[5:8]} {digits[8:]}"


def abn_checksum_ok(value: str | None) -> bool:
    """True when the ABR weighting sums to a multiple of 89."""
    try:
        digits = compact_abn(value)
        if not digits:
            return False
        # Inside the handler as well: a conversion failure here is invalid
        # input, and the predicate answers False rather than raising into
        # its caller.
        numbers = [int(d) for d in digits]
    except ValueError:
        return False
    numbers[0] -= 1
    total = sum(weight * digit for weight, digit in zip(_WEIGHTS, numbers, strict=True))
    return total % 89 == 0
