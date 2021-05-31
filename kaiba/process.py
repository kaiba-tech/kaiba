from typing import Union

from pydantic import ValidationError
from returns.functions import raise_exception
from returns.result import Failure, ResultE, safe

from kaiba.mapper import map_data
from kaiba.pydantic_schema import KaibaObject


def process(
    input_data: dict,
    configuration: dict,
) -> ResultE[Union[list, dict]]:
    """Validate configuration then process data."""
    cfg = KaibaObject(**configuration)
    return map_data(input_data, cfg)


def process_raise(
    input_data: dict,
    configuration: dict,
) -> Union[list, dict]:
    """Call Process and unwrap value if no error, otherwise raise."""
    return process(
        input_data,
        configuration,
    ).alt(
        raise_exception,
    ).unwrap()
