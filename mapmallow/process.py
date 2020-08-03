# -*- coding: utf-8 -*-

"""Process function to do everything."""
import decimal
from typing import Any

from attr import dataclass
from returns.curry import partial
from returns.pipeline import flow, is_successful
from returns.pointfree import bind
from returns.result import Result, safe
from typing_extensions import final

from mapmallow.configuration_schemas import ConfigObject
from mapmallow.mapper import Map
from mapmallow.schema import ApplySchema
from mapmallow.valuetypes import (
    CallableLogFunction,
    CallableMapFunction,
    CallableOutput,
    CallablePreProcess,
    CallableValidateAndMarshall,
)

# Set default rounding rule to ROUND_HALF_UP
decimal.getcontext().rounding = decimal.ROUND_HALF_UP


@safe
def return_arg(raw: Any) -> Any:
    """Help function to return argument but wrapped in @safe."""
    return raw


@final
@dataclass(frozen=True, slots=True)
class Process(object):
    """Process data with provided configuration.

    .. versionadded:: 0.1.6

    :param configuration: mapping configuration
    :type dict:

    :param raw_data: the data to map
    :type Any:
    """

    _validate_and_marshall: CallableValidateAndMarshall

    _pre_process: CallablePreProcess = return_arg
    _output: CallableOutput = return_arg

    _map: CallableMapFunction = Map()
    _log: CallableLogFunction = print  # noqa: T002
    _validate_configuration = ApplySchema(ConfigObject())

    def __call__(
        self,
        raw_data: Any,
        configuration: dict,
    ) -> Result[Any, Exception]:
        """Run code."""
        cfg_result = self._validate_configuration(configuration)

        if not is_successful(cfg_result):
            return cfg_result

        return flow(
            raw_data,
            self._pre_process,
            bind(partial(self._map, configuration=cfg_result.unwrap())),
            bind(self._validate_and_marshall),
            bind(self._output),
        )
