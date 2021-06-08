from enum import Enum
from typing import Optional

from pydantic import Field

from kaiba.models.base import AnyType, KaibaBaseModel


class Conditions(str, Enum):  # noqa: WPS600
    """Conditions for if statements."""

    IS = 'is'  # noqa: WPS115
    NOT = 'not'  # noqa: WPS115
    IN = 'in'  # noqa: WPS115
    CONTAINS = 'contains'  # noqa: WPS115


class IfStatement(KaibaBaseModel):
    """If statements lets you conditionally change data."""

    condition: Conditions
    target: Optional[AnyType] = Field(...)  # ... = required but allow None
    then: Optional[AnyType]  = Field(...)  # ... = required but allow Nones
    otherwise: Optional[AnyType] = None  # Should be any valid json value

    class Config:
        """Add json schema examples."""

        schema_extra = {
            'examples': [
                {
                    'condition': 'is',
                    'target': 'target value',
                    'then': 'was target value',
                },
                {
                    'condition': 'not',
                    'target': 'target_value',
                    'then': 'was not target value',
                    'otherwise': 'was target value',
                },
                {
                    'condition': 'in',
                    'target': ['one', 'of', 'these'],
                    'then': 'was either one, of or these',
                    'otherwise': 'was none of those',
                },
                {
                    'condition': 'in',
                    'target': 'a substring of this will be true',
                    'then': 'substrings also work',
                    'otherwise': 'was not a substring of target',
                },
                {
                    'condition': 'contains',
                    'target': 'value',
                    'then': 'value was a substring of input',
                    'otherwise': 'value was not in the input',
                },

            ]
        }
