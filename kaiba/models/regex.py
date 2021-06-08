from typing import List, Pattern, Union

from pydantic.types import StrictInt

from kaiba.models.base import KaibaBaseModel


class Regex(KaibaBaseModel):
    """Use regular expression on data found by data_fetchers."""

    expression: Pattern
    group: Union[StrictInt, List[StrictInt]] = 0

    class Config:
        """Add json schema examples."""

        schema_extra = {
            'examples': [
                {
                    'expression': '[a-z]+',
                },
                {
                    'expression': '([a-z])',
                    'group': [0, 3, 4],
                },
            ],
        }
