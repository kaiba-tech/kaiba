from typing import List, Pattern, Union

from pydantic.types import StrictInt

from kaiba.models.base import KaibaBaseModel


class Regex(KaibaBaseModel):
    """Use regular expression to find your data."""

    expression: Pattern
    group: Union[StrictInt, List[StrictInt]] = 0
