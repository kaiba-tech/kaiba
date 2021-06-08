from typing import Any, List, Optional

from pydantic import Field

from kaiba.models.base import KaibaBaseModel, StrInt
from kaiba.models.if_statement import IfStatement
from kaiba.models.regex import Regex
from kaiba.models.slice import Slice


class DataFetcher(KaibaBaseModel):
    """Data fetcher lets you fetch data from the input."""

    path: List[StrInt] = []
    slice_: Optional[Slice] = Field(alias='slice')
    regex: Optional[Regex]
    if_statements: List[IfStatement] = []
    default: Optional[Any]
