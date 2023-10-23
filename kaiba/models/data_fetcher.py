from typing import Any, List, Optional

from kaiba.models.base import KaibaBaseModel, StrInt
from kaiba.models.if_statement import IfStatement
from kaiba.models.regex import Regex
from kaiba.models.slicing import Slicing
from pydantic import ConfigDict


class DataFetcher(KaibaBaseModel):
    """Data fetcher lets you fetch data from the input."""

    path: List[StrInt] = []
    slicing: Optional[Slicing] = None
    regex: Optional[Regex] = None
    if_statements: List[IfStatement] = []
    default: Optional[Any] = None
    model_config = ConfigDict(json_schema_extra={
        'examples': [
            {
                'path': ['path', 'to', 'data'],
            },
            {
                'path': ['path', 1, 2, 'my_val'],
                'defualt': 'if no data was found this value is used',
            },
        ],
    })
