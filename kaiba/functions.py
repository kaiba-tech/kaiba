import re
from typing import Any, List, Optional, Union

from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import Failure, ResultE, safe

from kaiba.casting import get_casting_function
from kaiba.pydantic_schema import (
    AnyType,
    Casting,
    ConditionEnum,
    IfStatement,
    Regexp,
    Slicing,
)
from kaiba.valuetypes import ValueTypes


@safe
def apply_if_statements(
    if_value: Optional[AnyType],
    if_objects: List[IfStatement],
) -> Optional[AnyType]:
    """Apply if statements to a value.

    :param if_value: The value to use when evaluating if statements
    :type if_value: AnyType

    :param if_objects: :term:`if_objects` collection of if operations
    :type if_objects: List[Dict[str, Any]]

    :return: Success/Failure containers
    :rtype: AnyType

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
        >>> apply_if_statements(
        ...     '1', [
        ...         IfStatement(
        ...             **{'condition': 'is', 'target': '1', 'then': '2'}
        ...         )
        ...     ],
        ... ).unwrap() == '2'
        True
        >>> apply_if_statements(
        ...     'a',
        ...     [IfStatement(**{
        ...         'condition': 'is',
        ...         'target': '1',
        ...         'then': '2',
        ...         'otherwise': '3'
        ...     })],
        ... ).unwrap() == '3'
        True

    """
    for if_object in if_objects:

        if_value = _apply_statement(
            if_value, if_object,
        )

    if if_value is None:
        raise ValueError('If statement failed or produced `None`')

    return if_value


def _apply_statement(
    if_value: Optional[AnyType],
    if_object: IfStatement,
) -> Optional[AnyType]:
    evaluation: bool = False

    condition = if_object.condition
    target = if_object.target

    if condition == ConditionEnum.IS:
        evaluation = if_value == target

    if condition == ConditionEnum.NOT:
        evaluation = if_value != target

    if condition == ConditionEnum.IN:
        evaluation = if_value in target  # type: ignore

    if condition == ConditionEnum.CONTAINS:
        list_or_dict = isinstance(if_value, (dict, list))
        evaluation = list_or_dict and target in if_value  # type: ignore
        evaluation = evaluation or not list_or_dict and str(target) in str(if_value)  # noqa: E501 E262
    if evaluation:
        return if_object.then

    return if_object.otherwise or if_value


@safe
def apply_separator(
    mapped_values: List[AnyType],
    separator: str,
) -> AnyType:
    """Apply separator between the values of a List[Any].

    :param mapped_values: The list of values to join with the separator
    :type mapped_values: List[AnyType]

    :param separator: :term:`separator` value to join mapped_values list with
    :type separator: str

    :return: Success/Failure containers
    :rtype: AnyType

    Example
        >>> from returns.pipeline import is_successful
        >>> apply_separator(['a', 'b', 'c'], ' ').unwrap()
        'a b c'
        >>> apply_separator([1, 'b', True], ' ').unwrap()
        '1 b True'
        >>> is_successful(apply_separator([], ' '))
        False

    """
    if not mapped_values:
        raise ValueError('mapped_values is empty')

    if len(mapped_values) == 1:
        return mapped_values[0]

    return separator.join([str(mapped) for mapped in mapped_values])


def apply_slicing(
    value_to_slice: Optional[Any],
    slicing: Slicing,
) -> Optional[AnyType]:
    """Slice value from index to index.

    :param value_to_slice: The value to slice
    :type value_to_slice: Any

    :param slicing: :term:`slicing` object
    :type slicing: dict


    :return: Success/Failure containers
    :rtype: Any

    Example
        >>> apply_slicing('123', Slicing(**{'from': 1}))
        '23'
        >>> apply_slicing('test', Slicing(**{'from': 1, 'to': 3}))
        'es'
    """
    if value_to_slice is None:
        return value_to_slice

    if not slicing:
        return value_to_slice

    if not isinstance(value_to_slice, list):
        value_to_slice = str(value_to_slice)

    return value_to_slice[slicing.slice_from:slicing.slice_to]


@safe
def apply_regexp(  # noqa: WPS212, WPS234
    value_to_match: Optional[AnyType],
    regexp: Regexp,
) -> Union[List[AnyType], AnyType, None]:
    r"""Match value by a certain regexp pattern.

    :param value_to_match: The value to match
    :type value_to_match: AnyType

    :param regexp: :term: `matching` object which has parameters for
        regexp match
    :type regexp: dict

    :return: Success/Failure container
    :rtype: AnyType

    Example
        >>> from kaiba.functions import apply_regexp
        >>> apply_regexp('abcdef', Regexp(**{'search': '(?<=abc)def'})).unwrap()
        'def'
        >>> apply_regexp(
        ...     'Isaac Newton, physicist',
        ...     Regexp(**{'search': r'(\w+)', 'group': 1}),
        ... ).unwrap()
        'Newton'
        >>> apply_regexp(
        ...     'Isaac Newton, physicist',
        ...     Regexp(**{'search': r'(\w+)', 'group': [1, 2]}),
        ... ).unwrap()
        ['Newton', 'physicist']
        >>> apply_regexp(None, Regexp(**{'search': 'a+'})).unwrap()
        >>> apply_regexp('Open-source matters', None).unwrap()
        'Open-source matters'
    """
    if value_to_match is None:
        return value_to_match

    if not regexp or not regexp.search:
        return value_to_match

    pattern = regexp.search
    groups = re.finditer(pattern, value_to_match)
    matches: list = [gr.group(0) for gr in groups]
    num_group: Union[int, List[int]] = regexp.group
    if isinstance(num_group, list):
        if not num_group:
            return matches
        return [matches[ind] for ind in num_group]  # typing: ignore
    return matches[num_group]


def apply_casting(
    value_to_cast: Optional[AnyType],
    casting: Casting,
) -> ResultE[AnyType]:
    """Cast one type of code to another.

    :param casting: :term:`casting` object
    :type casting: dict

    :param value_to_cast: The value to cast to casting['to']
    :type value_to_cast: AnyType

    :return: Success/Failure containers
    :rtype: AnyType

    Example
        >>> apply_casting('123', Casting(**{'to': 'integer'})).unwrap()
        123
        >>> apply_casting('123.12', Casting(**{'to': 'decimal'})).unwrap()
        Decimal('123.12')
    """
    if value_to_cast is None:
        return Failure(ValueError('value_to_cast is empty'))

    return flow(
        casting.to,
        get_casting_function,
        bind(  # type: ignore
            lambda function: function(  # type: ignore
                value_to_cast, casting.original_format,
            ),
        ),
    )


@safe
def apply_default(
    mapped_value: Optional[AnyType] = None,
    default: Optional[AnyType] = None,
) -> AnyType:
    """Apply default value if exists and if mapped value is None.

    :param mapped_value: If this value is *None* the default value is returned
    :type mapped_value: Optional[AnyType]

    :param default: :term:`default` value to return if mapped value is None
    :type default: Optional[AnyType]

    :return: Success/Failure containers
    :rtype: AnyType

    If default *is not* none and mapped_value *is* None then return default
    else if mapped_value is not in accepted ValueTypes then throw an error
    else return mapped value

    Example
        >>> apply_default('test', None).unwrap() == 'test'
        True
        >>> apply_default('nope', 'test').unwrap() == 'nope'
        True
    """
    if default is not None:
        if mapped_value is None:
            return default

    if mapped_value is None:
        raise ValueError('Default value should not be `None`')

    if not isinstance(mapped_value, ValueTypes):
        raise ValueError('Unable to give default value')

    return mapped_value
