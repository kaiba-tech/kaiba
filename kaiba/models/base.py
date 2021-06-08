from decimal import Decimal
from typing import Union

from pydantic import BaseModel, Extra
from pydantic.types import StrictBool, StrictInt, StrictStr

AnyType = Union[StrictStr, StrictInt, StrictBool, Decimal, list, dict]
StrInt = Union[StrictStr, StrictInt]


class KaibaBaseModel(BaseModel):
    """Allows for iterating lists at given path."""

    class Config(object):
        """Make sure any unexpected attributes in config cause error."""

        extra = Extra.forbid
