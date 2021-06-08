from enum import Enum
from typing import Optional

from pydantic import Field

from kaiba.models.base import AnyType, KaibaBaseModel


class ConditionOptions(str, Enum):  # noqa: WPS600
    """Conditions for if statements."""

    IS = 'is'  # noqa: WPS115
    NOT = 'not'  # noqa: WPS115
    IN = 'in'  # noqa: WPS115
    CONTAINS = 'contains'  # noqa: WPS115


class IfStatement(KaibaBaseModel):
    """Handles if statements."""

    condition: ConditionOptions
    target: Optional[AnyType] = Field(...)  # ... = required but allow None
    then: Optional[AnyType]  = Field(...)  # ... = required but allow Nones
    otherwise: Optional[AnyType] = None  # Should be any valid json value
