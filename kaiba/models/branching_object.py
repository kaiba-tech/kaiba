from typing import List

from pydantic import ConfigDict
from pydantic.types import StrictBool

from kaiba.models.attribute import Attribute
from kaiba.models.base import KaibaBaseModel
from kaiba.models.iterator import Iterator


class BranchingObject(KaibaBaseModel):
    """Lets you branch out attribute mappings.

    The branching object is a special kind of object where you can have
    different attributes per instance.

    ie:
    {
        "extra_fields": [
            {
                "name": "field1",
                "value": "value at path x",
            },
            {
                "name": "field2",
                "value": "value at path y"
            },
            {
                "other_key": "whatever you want",
            }
        ]
    }

    Whereas normal objects you'd have to have both `name`, `value` and
    `other_key` in all instances.
    """

    name: str
    array: StrictBool = False
    iterators: List[Iterator] = []
    branching_attributes: List[List[Attribute]] = []
    model_config = ConfigDict(json_schema_extra={
        'examples': [
            {
                'name': 'extra_fields',
                'array': True,
                'branching_attributes': [
                    [
                        {
                            'name': 'field_name',
                            'default': 'amount',
                        },
                        {
                            'name': 'field_data',
                            'data_fetchers': [
                                {
                                    'path': ['path', 'to', 'amount'],
                                },
                            ],
                        },
                    ],
                    [
                        {
                            'name': 'field_name',
                            'default': 'currency',
                        },
                        {
                            'name': 'field_data',
                            'data_fetchers': [
                                {
                                    'path': ['path', 'to', 'currency'],
                                },
                            ],
                            'default': 'NOK',
                        },
                    ],
                ],
            },
        ],
    })
