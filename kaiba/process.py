from typing import Callable, Union

from attr import dataclass
from pydantic import ValidationError
from returns.functions import raise_exception
from returns.pipeline import is_successful
from returns.result import ResultE, Failure
from typing_extensions import final

from kaiba.mapper import map_data
from kaiba.schema import SchemaValidator
from kaiba.pydantic_schema import KaibaObject


@final
@dataclass(frozen=True, slots=True)
class Process(object):
    """Process Callable Object."""

    validate: Callable[[dict], ResultE[dict]] = SchemaValidator()

    def __call__(
        self,
        input_data: dict,
        configuration: dict,
    ) -> ResultE[Union[list, dict]]:
        """Validate configuration then process data."""
        # cfg = self.validate(configuration)

        try:
            cfg = KaibaObject(**configuration)
        except ValidationError as ve:
            return Failure(ve)

        # if not is_successful(cfg):
        #    return cfg

        return map_data(input_data, cfg)


def process(
    input_data: dict,
    configuration: dict,
) -> Union[list, dict]:
    """Call Process and unwrap value if no error, otherwise raise."""
    return Process()(
        input_data,
        configuration,
    ).alt(
        raise_exception,
    ).unwrap()
