from enum import Enum
from typing import Optional

from kaiba.models.base import KaibaBaseModel


class CastToOptions(str, Enum):  # noqa: WPS600
    """Types that we can cast a value to."""

    STRING = 'string'  # noqa: WPS115
    INTEGER = 'integer'  # noqa: WPS115
    DECIMAL = 'decimal'  # noqa: WPS115
    DATE = 'date'  # noqa: WPS115


class Cast(KaibaBaseModel):
    """Allows user to cast to type."""

    to: CastToOptions
    original_format: Optional[str] = None
