from typing import Any, List, Optional

from pydantic import Field

from kaiba.models.base import KaibaBaseModel, StrInt
from kaiba.models.if_statement import IfStatement
from kaiba.models.regex import Regex
from kaiba.models.slicing import Slicing


class DataFetcher(KaibaBaseModel):
    """Data fetcher lets you fetch data from the input."""

    path: List[StrInt] = []
    slice_: Optional[Slicing] = Field(alias='slice')
    regex: Optional[Regex]
    if_statements: List[IfStatement] = []
    default: Optional[Any]

    class Config:
        """Add json schema examples."""

        schema_extra = {
            'examples': [
                {
                    'path': ['path', 'to', 'data'],
                },
                {
                    'path': ['path', 1, 2, 'my_val'],
                    'defualt': 'if no data was found this value is used',
                },
            ],
        }
