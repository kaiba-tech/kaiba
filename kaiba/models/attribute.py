from typing import List, Optional

from pydantic import ConfigDict

from kaiba.models.base import AnyType, KaibaBaseModel
from kaiba.models.casting import Casting
from kaiba.models.data_fetcher import DataFetcher
from kaiba.models.if_statement import IfStatement


class Attribute(KaibaBaseModel):
    """Adds an attribute with the given name."""

    name: str
    data_fetchers: List[DataFetcher] = []
    separator: str = ''
    if_statements: List[IfStatement] = []
    casting: Optional[Casting] = None
    default: Optional[AnyType] = None
    model_config = ConfigDict(json_schema_extra={
        'examples': [
            {
                'name': 'my_attribute',
                'data_fetchers': [{
                    'path': ['abc', 0],
                }],
                'default': 'default_value',
            },
        ],
    })
