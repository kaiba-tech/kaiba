# -*- coding: utf-8 -*-

"""Mapping functions for GBGO."""
import decimal
from typing import Any, Callable, Dict, List, Optional

from attr import dataclass
from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import Failure, ResultE, Success, safe
from typing_extensions import final

from mapmallow.casting import CastToDate, CastToDecimal, CastToInteger
from mapmallow.constants import (  # noqa: WPS235
    CONDITION,
    CONTAINS,
    DATE,
    DECIMAL,
    INTEGER,
    IS,
    NOT,
    ORIGINAL_FORMAT,
    OTHERWISE,
    TARGET,
    THEN,
    TO,
)
from mapmallow.valuetypes import MapValue, ValueTypes


@final
@dataclass(frozen=True, slots=True)
class ApplyIfStatements(object):
    """Apply if statements to a value.

    .. versionadded:: 0.1.0

    :param if_objects: :term:`if_objects` collection of if operations
    :type if_objects: Dict[str, Any]

    :param if_value: The value to use when evaluating if statements
    :type if_value: MapValue

    :return: Success/Failure containers
    :rtype: MapValue

    one if object looks like this

    .. code-block:: json

        {
            "condition": "is",
            "target": "foo",
            "then": "bar",
            "otherwise": "no foo" - optional
        }

    The if statements are chained so that the next works on the output of the
    previous. If no "otherwise" is provided then the original value or value
    from the previous operation will be returned.

    Example
        >>> apply_ifs = ApplyIfStatements()
        >>> apply_ifs(
        ...     '1', [{'condition': 'is', 'target': '1', 'then': '2'}],
        ... ).unwrap() == '2'
        True
        >>> apply_ifs(
        ...     'a',
        ...     [{
        ...         'condition': 'is',
        ...         'target': '1',
        ...         'then': '2',
        ...         'otherwise': '3'
        ...     }],
        ... ).unwrap() == '3'
        True

    """

    @safe
    def __call__(
        self,
        if_value: Optional[MapValue],
        if_objects: List[Dict[str, Any]],
    ) -> MapValue:
        """Make this object callable."""
        for if_object in if_objects:

            if_value = self._apply_statement(
                if_value, if_object,
            ).value_or(if_value)  # type: ignore

        if if_value is None:
            raise ValueError('If statement failed or produced `None`')

        return if_value

    @safe
    def _apply_statement(
        self,
        if_value: Optional[MapValue],
        if_object: Dict[str, Any],
    ) -> Optional[MapValue]:
        evaluation: bool = False

        condition = if_object[CONDITION]

        if condition == IS:
            evaluation = if_value == if_object[TARGET]

        if condition == NOT:
            evaluation = if_value != if_object[TARGET]

        if condition == CONTAINS:
            evaluation = if_object[TARGET] in str(if_value)

        if evaluation:
            return if_object[THEN]

        return if_object.get(OTHERWISE, if_value)


@final
@dataclass(frozen=True, slots=True)
class ApplySeparator(object):
    """Apply separator between the values of a List[Any].

    .. versionadded:: 0.1.0

    :param separator: :term:`separator` value to join mapped_values list with
    :type separator: str

    :param mapped_values: The list of values to join with the separator
    :type mapped_values: List[MapValue]

    :return: Success/Failure containers
    :rtype: MapValue

    Example
        >>> from returns.pipeline import is_successful
        >>> separate = ApplySeparator()
        >>> separate(['a', 'b', 'c'], ' ').unwrap()
        'a b c'
        >>> separate([1, 'b', True], ' ').unwrap()
        '1 b True'
        >>> is_successful(separate([], ' '))
        False

    """

    @safe
    def __call__(
        self,
        mapped_values: List[MapValue],
        separator: str,
    ) -> MapValue:
        """Return default if default is not None and mapped value _is_ None."""
        if not mapped_values:
            raise ValueError('mapped_values is empty')

        if len(mapped_values) == 1:
            return mapped_values[0]

        return separator.join([str(mapped) for mapped in mapped_values])


@final
@dataclass(frozen=True, slots=True)
class ApplyCasting(object):
    """Cast one type of code to another.

    :param casting: :term:`casting` object
    :type casting: dict

    :param value_to_cast: The value to cast to casting['to']
    :type value_to_cast: MapValue

    :return: Success/Failure containers
    :rtype: MapValue

    Example
        >>> cast = ApplyCasting()
        >>> cast('123', {'to': 'integer'}).unwrap()
        123
        >>> cast('123.12', {'to': 'decimal'}).unwrap()
        Decimal('123.12')
    """

    decimal.getcontext().rounding = decimal.ROUND_HALF_UP

    _cast_to_date: Callable = CastToDate()
    _cast_to_decimal: Callable = CastToDecimal()
    _cast_to_integer: Callable = CastToInteger()

    def __call__(
        self,
        value_to_cast: Optional[MapValue],
        casting: Dict[str, Any],
    ) -> ResultE[MapValue]:
        """Return default if default is not None and mapped value _is_ None."""
        if not value_to_cast:
            return Failure(ValueError('value_to_cast is empty'))

        if TO not in casting or casting[TO] is None:
            return Success(value_to_cast)

        return flow(
            casting[TO],
            self._get_casting_function,
            bind(  # type: ignore
                lambda function: function(  # type: ignore
                    value_to_cast, casting.get(ORIGINAL_FORMAT),
                ),
            ),
        )

    @safe
    def _get_casting_function(self, cast_to: str) -> Callable:

        if cast_to == INTEGER:
            return self._cast_to_integer

        elif cast_to == DECIMAL:
            return self._cast_to_decimal

        elif cast_to == DATE:
            return self._cast_to_date

        raise NotImplementedError(
            'Unsupported cast to value ({0})'.format(cast_to),
        )


@final
@dataclass(frozen=True, slots=True)
class ApplyDefault(object):
    """Apply default value if exists if mapped value is None.

    .. versionadded:: 0.1.0

    :param default: :term:`default` value to return if mapped value is None
    :type default: Optional[MapValue]

    :param mapped_value: If this value is *None* the default value is returned
    :type mapped_value: Optional[MapValue]

    :return: Success/Failure containers
    :rtype: MapValue

    If default *is not* none and mapped_value *is* None then return default
    else if mapped_value is not in accepted ValueTypes then throw an error
    else return mapped value

    Example
        >>> apply = ApplyDefault()
        >>> apply('test', None).unwrap() == 'test'
        True
        >>> apply('nope', 'test').unwrap() == 'nope'
        True
    """

    @safe
    def __call__(
        self,
        mapped_value: Optional[Any] = None,
        default: Optional[MapValue] = None,
    ) -> MapValue:
        """Return default if default is not None and mapped value _is_ None."""
        if default is not None:
            if mapped_value is None:
                return default

        if mapped_value is None:
            raise ValueError('Default value should not be `None`')

        if not isinstance(mapped_value, ValueTypes):
            raise ValueError('Unable to give default value')

        return mapped_value
