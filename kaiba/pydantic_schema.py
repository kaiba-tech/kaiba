from decimal import Decimal
from enum import Enum
from typing import Any, List, Optional, Pattern, Union

from pydantic import BaseModel, Field
from pydantic.types import StrictBool, StrictInt, StrictStr

AnyType = Union[StrictStr, StrictInt, StrictBool, Decimal, list, dict]
StrInt = Union[StrictStr, StrictInt]


class Iterable(BaseModel):
    """Allows for iterating lists at given path."""

    alias: str
    path: List[StrInt] = Field(..., min_items=1)


class Regexp(BaseModel):
    """Use regular expression to find your data."""

    search: Pattern
    group: Union[StrictInt, List[StrictInt]] = 0


class Slicing(BaseModel):
    """Slice from inclusive to exclusive like python slice."""

    slice_from: StrictInt = Field(alias='from')
    slice_to: Optional[StrictInt] = Field(None, alias='to')


class CastingEnum(str, Enum):  # noqa: WPS600
    """Types that we can cast a value to."""

    STRING = 'string'  # noqa: WPS115
    INTEGER = 'integer'  # noqa: WPS115
    DECIMAL = 'decimal'  # noqa: WPS115
    DATE = 'date'  # noqa: WPS115


class Casting(BaseModel):
    """Allows user to cast to type."""

    to: CastingEnum
    original_format: Optional[str] = None


class ConditionEnum(str, Enum):  # noqa: WPS600
    """Conditions for if statements."""

    IS = 'is'  # noqa: WPS115
    NOT = 'not'  # noqa: WPS115
    IN = 'in'  # noqa: WPS115
    CONTAINS = 'contains'  # noqa: WPS115


class IfStatement(BaseModel):
    """Handles if statements."""

    condition: ConditionEnum
    target: Optional[AnyType]  # Should be any valid json value
    then: Optional[AnyType]  # Should be any valid json value
    otherwise: Optional[AnyType] = None  # Should be any valid json value


class Mapping(BaseModel):
    """Mapping actually finds data at given path."""

    path: List[StrInt] = []
    slicing: Optional[Slicing]
    regexp: Optional[Regexp]
    if_statements: List[IfStatement] = []
    default: Optional[Any]


class Attribute(BaseModel):
    """Create an attribute for an object."""

    name: str
    mappings: List[Mapping] = []
    separator: str = ''
    if_statements: List[IfStatement] = []
    casting: Optional[Casting]
    default: Optional[AnyType] = None


class BranchingObject(BaseModel):
    """Branching object model."""

    name: str
    array: StrictBool = False
    iterables: List[Iterable] = []
    branching_attributes: List[List[Attribute]] = []


class KaibaObject(BaseModel):
    """Our main object."""

    name: str
    array: StrictBool = False
    iterables: List[Iterable] = []
    attributes: List[Attribute] = []
    objects: List['KaibaObject'] = []  # noqa: WPS110
    branching_objects: List[BranchingObject] = []


KaibaObject.update_forward_refs()
