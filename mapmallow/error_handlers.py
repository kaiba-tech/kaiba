# -*- coding: utf-8 -*-

"""Collection of Functions that can be provided to ValidateAndOutput.

All functions here will receive an original_value and an error message.

regexes should be used to match the error message too see if its a message that
the function is made to handle. if not return original value.
"""
import re
from typing import List, Optional

from attr import dataclass
from returns.result import safe
from typing_extensions import final

from mapmallow.valuetypes import MapValue


@safe
def error_dict_as_list_of_tuples(
    error_dict,
    path: tuple = (),
) -> List[tuple]:
    """Format an marshmallow error dictionary to a list of paths.

    The actual errors are a list of strings at the end of 1..n keys in a dict.
    """
    paths = []

    for key, errors in error_dict.items():
        if isinstance(errors, list):
            paths.append((*path, key))

        else:
            recursion_call = error_dict_as_list_of_tuples(
                errors, (*path, key),
            ).unwrap()
            for res in recursion_call:
                paths.append(res)

    return paths


@final
@dataclass(frozen=True, slots=True)
class CastToStringUnlessNone(object):
    """Casts values to string unless its None.

    Error match: `^Not a valid string.$`

    .. versionadded:: 0.1.0

    :param original_value: value to cast to string
    :type original_value: Dict[str, Any]

    :param error: error pattern must match this or it wasnt the error we wanted
    :type error: str

    :return: Success/Failure containers
    :rtype: MapValue

    Example
        >>> error = 'Not a valid string.'
        >>> CastToStringUnlessNone()(None, error).unwrap()
        >>> CastToStringUnlessNone()(1, error).unwrap()
        '1'
        >>> CastToStringUnlessNone()(True, error).unwrap()
        'True'
        >>> CastToStringUnlessNone()(1, 'wrong error').unwrap()
        1

    """

    _pattern = re.compile(r'^Not a valid string.$')

    @safe
    def __call__(
        self, original_value: Optional[MapValue], error: str, *args, **kwargs,
    ) -> Optional[MapValue]:
        """Match pattern and get max length and return cut string."""
        match = self._pattern.match(error)
        if match:
            if original_value is None:
                return original_value

            return str(original_value)

        return original_value


@final
@dataclass(frozen=True, slots=True)
class CutStringsWhenTooLong(object):
    r"""Fixer for when strings are too long and you can cut them.

    Error match: `^Longer than maximum length (\d+).$`

    .. versionadded:: 0.1.0

    :param original_value: value to cut
    :type original_value: Dict[str, Any]

    :param error: error pattern must match this or it wasnt the error we wanted
    :type error: str

    :return: Success/Failure containers
    :rtype: MapValue

    Example
        >>> error = 'Longer than maximum length '
        >>> CutStringsWhenTooLong()('bob', error + '2.').unwrap()
        'bo'
        >>> CutStringsWhenTooLong()(1, error + '4.').unwrap()
        '1'
        >>> CutStringsWhenTooLong()(True, error + '2.').unwrap()
        'Tr'
        >>> CutStringsWhenTooLong()(1, 'wrong error').unwrap()
        1

    """

    _pattern = re.compile(r'^Longer than maximum length (\d+).$')

    @safe
    def __call__(
        self, original_value: MapValue, error: str, *args, **kwargs,
    ) -> MapValue:
        """Match pattern and get max length and return cut string."""
        match = self._pattern.match(error)
        if match:
            max_length = int(match[1])
            return str(original_value)[:max_length]

        return original_value
