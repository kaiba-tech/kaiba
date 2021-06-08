from typing import List

from pydantic.types import StrictBool

from kaiba.models.attribute import Attribute
from kaiba.models.base import KaibaBaseModel
from kaiba.models.iterator import Iterator


class BranchingObject(KaibaBaseModel):
    """Branching object model."""

    name: str
    array: StrictBool = False
    iterators: List[Iterator] = []
    branching_attributes: List[List[Attribute]] = []
