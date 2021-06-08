from typing import List, Optional

from kaiba.models.base import AnyType, KaibaBaseModel
from kaiba.models.cast import Cast
from kaiba.models.data_fetcher import DataFetcher
from kaiba.models.if_statement import IfStatement


class Attribute(KaibaBaseModel):
    """Adds an attribute with the given name."""

    name: str
    data_fetchers: List[DataFetcher] = []
    separator: str = ''
    if_statements: List[IfStatement] = []
    cast: Optional[Cast]
    default: Optional[AnyType] = None

    class Config:
        """Add json schema examples."""

        schema_extra = {
            'examples': [
                {
                    'name': 'my_attribute',
                    'data_fetchers': [{
                        'path': ['abc', 0]
                    }],
                    'default': 'default_value',
                },
            ],
        }
