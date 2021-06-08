from typing import List

from pydantic import Field

from kaiba.models.base import KaibaBaseModel, StrInt


class Iterator(KaibaBaseModel):
    """Allows for iterating lists at given path."""

    alias: str
    path: List[StrInt] = Field(..., min_items=1)

    class Config:
        """Add json schema examples."""

        schema_extra = {
            'examples': [
                {
                    'alias': 'an_item',
                    'path': ['path', 'to', 10, 'data']
                },
            ]
        }
