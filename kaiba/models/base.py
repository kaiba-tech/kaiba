from decimal import Decimal
from typing import Union

from pydantic import BaseModel, ConfigDict
from pydantic.types import StrictBool, StrictInt, StrictStr

AnyType = Union[StrictStr, StrictInt, StrictBool, Decimal, list, dict]
StrInt = Union[StrictStr, StrictInt]


class KaibaBaseModel(BaseModel):
    """Base model that forbids non defined attributes."""

    model_config = ConfigDict(extra='forbid')
