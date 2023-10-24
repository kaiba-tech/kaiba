from __future__ import annotations

import re
from decimal import Decimal

from returns.result import safe
from typing_extensions import Final

from kaiba.constants import COMMA, EMPTY, INTEGER_CONTAINING_DECIMALS, PERIOD
from kaiba.models.base import AnyType

_decimal_pattern: Final = re.compile(r'^([0-9]|-|\.|,)+$')
_decimal_with_period_after_commas: Final = re.compile(r'^-?(\d+\,)*\d+\.\d+$')
_decimal_with_comma_after_periods: Final = re.compile(r'^-?(\d+\.)*\d+\,\d+$')


@safe
def cast_to_decimal(
    value_to_cast: AnyType,
    original_format: str | None = None,
) -> Decimal:
    """Cast input to decimal."""
    the_value = str(value_to_cast).replace(' ', EMPTY)

    if not _decimal_pattern.match(the_value):
        raise ValueError(
            "Illegal characters in value '{0}'".format(the_value),
        )

    if original_format == INTEGER_CONTAINING_DECIMALS:
        return Decimal(the_value) / 100

    # ie 1234567,89 only comma as decimal separator
    if the_value.count(COMMA) == 1 and not the_value.count(PERIOD):
        return Decimal(the_value.replace(COMMA, PERIOD))

    # ie 1,234,567.89 many commas followed by one period
    if _decimal_with_period_after_commas.match(the_value):
        return Decimal(the_value.replace(COMMA, EMPTY))

    # ie 1.234.567,89 many periods followed by one comma
    if _decimal_with_comma_after_periods.match(the_value):
        return Decimal(
            the_value.replace(PERIOD, EMPTY).replace(COMMA, PERIOD),
        )

    return Decimal(the_value)
