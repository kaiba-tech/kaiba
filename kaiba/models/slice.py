from typing import Optional

from pydantic import Field
from pydantic.types import StrictInt

from kaiba.models.base import KaibaBaseModel


class Slice(KaibaBaseModel):
    """Slice from inclusive to exclusive like python slice."""

    slice_from: StrictInt = Field(alias='from')
    slice_to: Optional[StrictInt] = Field(None, alias='to')
