from typing import Callable

from returns.result import safe


from kaiba.models.casting import CastToOptions

from kaiba.casting._cast_to_integer import cast_to_integer
from kaiba.casting._cast_to_decimal import cast_to_decimal
from kaiba.casting._cast_to_date import cast_to_date


@safe
def get_casting_function(cast_to: CastToOptions) -> Callable:
    """Return casting function depending on name."""
    if cast_to == CastToOptions.INTEGER:
        return cast_to_integer

    elif cast_to == CastToOptions.DECIMAL:
        return cast_to_decimal

    return cast_to_date
