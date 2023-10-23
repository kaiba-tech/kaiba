from typing import List

from pydantic import ConfigDict, Field

from kaiba.models.base import KaibaBaseModel, StrInt


class Iterator(KaibaBaseModel):
    """Allows for iterating lists at given path."""

    alias: str
    path: List[StrInt] = Field(..., min_length=1)
    model_config = ConfigDict(json_schema_extra={
        'examples': [
            {
                'alias': 'an_item',
                'path': ['path', 'to', 10, 'data'],
            },
        ],
    })
