# Copyright 2026 Ryan Duguid
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Standard Australian income year: 1 July to 30 June.

Substituted accounting periods exist. This helper is the standard year
only. It is not FBT year (1 April – 31 March) and it is not lodgment
advice.
"""

from __future__ import annotations

from datetime import date, datetime


def _as_date(day: date | datetime) -> date:
    if isinstance(day, datetime):
        return day.date()
    return day


def income_year_bounds(day: date | datetime) -> tuple[date, date]:
    """Return (start, end) of the standard AU income year containing day."""
    current = _as_date(day)
    if current.month > 6:
        start = date(current.year, 7, 1)
        end = date(current.year + 1, 6, 30)
    else:
        start = date(current.year - 1, 7, 1)
        end = date(current.year, 6, 30)
    return start, end


def income_year_label(day: date | datetime) -> str:
    """Return 'YYYY-YY', e.g. 1 July 2026 → '2026-27'."""
    start, _end = income_year_bounds(day)
    return f"{start.year}-{str(start.year + 1)[-2:]}"


def is_standard_income_year_end(month: int | str, day: int) -> bool:
    """True when the fiscal-year last day is 30 June."""
    return int(month) == 6 and int(day) == 30
