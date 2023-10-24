from __future__ import annotations

import decimal

from returns.pipeline import flow
from returns.pointfree import map_
from returns.result import ResultE

from kaiba.casting._cast_to_decimal import cast_to_decimal  # noqa: WPS436
from kaiba.models.base import AnyType


def cast_to_integer(
    value_to_cast: AnyType,
    original_format: str | None = None,
) -> ResultE[int]:
    """Cast input to integer."""
    return flow(
        value_to_cast,
        cast_to_decimal,
        map_(_quantize_decimal),
        map_(int),
    )


def _quantize_decimal(number: decimal.Decimal) -> decimal.Decimal:
    """Quantize a decimal to whole number."""
    return number.quantize(decimal.Decimal('1.'))
