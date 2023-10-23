from typing import List

from pydantic.types import StrictBool

from kaiba.models.attribute import Attribute
from kaiba.models.base import KaibaBaseModel
from kaiba.models.branching_object import BranchingObject
from kaiba.models.iterator import Iterator
from pydantic import ConfigDict


class KaibaObject(KaibaBaseModel):
    """Our main object."""

    name: str
    array: StrictBool = False
    iterators: List[Iterator] = []
    attributes: List[Attribute] = []
    objects: List['KaibaObject'] = []  # noqa: WPS110
    branching_objects: List[BranchingObject] = []
    model_config = ConfigDict(json_schema_extra={
        'examples': [
            {
                'name': 'object_name',
                'attributes': [
                    {
                        'name': 'an_attribute',
                        'default': 'a value',
                    },
                ],
            },
        ],
    })


KaibaObject.update_forward_refs()
