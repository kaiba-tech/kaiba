from enum import Enum
from typing import Any, List, Optional, Pattern, Union

from pydantic import BaseModel, Field


class Iterable(BaseModel):
    """Allows for iterating lists at given path."""

    alias: str
    path: List[Union[str, int]]


class Regexp(BaseModel):
    """Use regular expression to find your data."""

    search: Pattern
    group: Optional[Union[int, List[int]]] = 0  # noqa: WPS234


class Slicing(BaseModel):
    """Slice from inclusive to exclusive like python slice."""

    slice_from: int = Field(alias='from')
    slice_to: Optional[int] = Field(None, alias='to')


class CastingToEnum(Enum):
    """Types that we can cast a value to."""

    string = 'string'
    integer = 'integer'
    decimal = 'decimal'
    date = 'date'


class Casting(BaseModel):
    """Allows user to cast to type."""

    to: CastingToEnum
    original_format: Optional[str] = None


class IfStatementConditionEnum(Enum):
    """Conditions for if statements."""

    _is = 'is'
    _not = 'not'
    _in = 'in'
    _contains = 'contains'


class IfStatement(BaseModel):
    """Handles if statements."""

    condition: IfStatementConditionEnum
    target: Any  # Should be any valid json value
    then: Any  # Should be any valid json value
    otherwise: Optional[Any] = None  # Should be any valid json value


class Mapping(BaseModel):
    """Mapping actually finds data at given path."""

    path: List[Union[str, int]]
    slicing: Optional[Slicing]
    regexp: Optional[Regexp]
    if_statements: Optional[List[IfStatement]]
    default: Optional[Any] = None


class Attribute(BaseModel):
    """Create an attribute for an object."""

    name: str
    mappings: List[Mapping] = []
    separator: Optional[str]
    if_statements: List[IfStatement] = []
    casting: Optional[Casting]
    default: Optional[str] = None


class BranchingObject(BaseModel):
    """Branching object model."""

    name: str
    array: bool = False
    iterables: Optional[List[Iterable]] = []
    branching_attributes: List[List[Attribute]]


class KaibaObject(BaseModel):
    """Our main object."""

    name: str
    array: bool = False
    iterables: List[Iterable] = []
    attributes: List[Attribute] = []
    objects: List['KaibaObject'] = []  # noqa: WPS110
    branching_objects: List[BranchingObject] = []


KaibaObject.update_forward_refs()
