from typing import List, Pattern, Union

from pydantic.types import StrictInt

from kaiba.models.base import KaibaBaseModel
from pydantic import ConfigDict


class Regex(KaibaBaseModel):
    """Use regular expression on data found by data_fetchers."""

    expression: Pattern
    group: Union[StrictInt, List[StrictInt]] = 0
    model_config = ConfigDict(json_schema_extra={
        'examples': [
            {
                'expression': '[a-z]+',
            },
            {
                'expression': '([a-z])',
                'group': [0, 3, 4],
            },
        ],
    })
