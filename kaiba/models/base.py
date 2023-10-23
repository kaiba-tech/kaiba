from decimal import Decimal
from typing import Union

from pydantic import BaseModel, Extra
from pydantic.types import StrictBool, StrictInt, StrictStr

AnyType = Union[StrictStr, StrictInt, StrictBool, Decimal, list, dict]
StrInt = Union[StrictStr, StrictInt]


class KaibaBaseModel(BaseModel):
    """Allows for iterating lists at given path."""

    # TODO[pydantic]: The `Config` class inherits from another class, please create the `model_config` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    class Config(object):
        """Make sure any unexpected attributes in config cause error."""

        extra = Extra.forbid
