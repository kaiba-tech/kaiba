import re
from decimal import Decimal
from typing import Any, List, Optional, Union

from returns.pipeline import flow, is_successful
from returns.pointfree import bind
from returns.result import Failure, ResultE, safe
from returns.functions import raise_exception

from kaiba.casting import get_casting_function, unsafe_get_casting_function
from kaiba.models.base import AnyType
from kaiba.models.casting import Casting
from kaiba.models.if_statement import Conditions, IfStatement
from kaiba.models.regex import Regex
from kaiba.models.slicing import Slicing

ValueTypes = (str, int, float, bool, Decimal)


def apply_if_statements(
    if_value: Optional[AnyType],
    statements: List[IfStatement],
) -> Optional[AnyType]:
    """Apply if statements to a value.

    :param if_value: The value to use when evaluating if statements
    :type if_value: AnyType

    :param statements: :term:`statements` collection of if operations
    :type statements: List[Dict[str, Any]]

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
    for statement in statements:

        if_value = _apply_statement(
            if_value, statement,
        )

    return if_value


@safe
def old_apply_if_statements(
    if_value: Optional[AnyType],
    statements: List[IfStatement],
) -> Optional[AnyType]:
    """Apply if statements to a value.

    :param if_value: The value to use when evaluating if statements
    :type if_value: AnyType

    :param statements: :term:`statements` collection of if operations
    :type statements: List[Dict[str, Any]]

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
    for statement in statements:

        if_value = _apply_statement(
            if_value, statement,
        )

    if if_value is None:
        raise ValueError('If statement failed or produced `None`')

    return if_value


def _apply_statement(
    if_value: Optional[AnyType],
    statement: IfStatement,
) -> Optional[AnyType]:
    evaluation: bool = False

    condition = statement.condition
    target = statement.target

    if condition == Conditions.IS:
        evaluation = if_value == target

    if condition == Conditions.NOT:
        evaluation = if_value != target

    if condition == Conditions.IN:
        evaluation = if_value in target  # type: ignore

    if condition == Conditions.CONTAINS:
        list_or_dict = isinstance(if_value, (dict, list))
        evaluation = list_or_dict and target in if_value  # type: ignore
        evaluation = evaluation or not list_or_dict and str(target) in str(if_value)  # noqa: E501 E262
    if evaluation:
        return statement.then

    return statement.otherwise or if_value


def unsafe_apply_separator(
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

    if len(mapped_values) == 1:
        return mapped_values[0]

    return separator.join([str(mapped) for mapped in mapped_values])


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
    value_to_slice: Any,
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


def unsafe_apply_regex(  # noqa: WPS212, WPS234
    value_to_match: AnyType,
    regex: Regex,
) -> Union[List[AnyType], AnyType, None]:
    r"""Match value by a certain regex pattern.

    :param value_to_match: The value to match
    :type value_to_match: AnyType

    :param regex: :term: `matching` object which has parameters for
        regex match
    :type regex: Regex

    :return: Success/Failure container
    :rtype: AnyType

    Example
        >>> apply_regex(
        ...     'abcdef',
        ...     Regex(**{'expression': '(?<=abc)def'})
        ... ).unwrap()
        'def'
        >>> apply_regex(
        ...     'Isaac Newton, physicist',
        ...     Regex(**{'expression': r'(\w+)', 'group': 1}),
        ... ).unwrap()
        'Newton'
        >>> apply_regex(
        ...     'Isaac Newton, physicist',
        ...     Regex(**{'expression': r'(\w+)', 'group': [1, 2]}),
        ... ).unwrap()
        ['Newton', 'physicist']
        >>> apply_regex(None, Regex(**{'expression': 'a+'})).unwrap()
        >>> apply_regex('Open-source matters', None).unwrap()
        'Open-source matters'
    """
    pattern = regex.expression
    groups = re.finditer(pattern, value_to_match)
    matches = [gr.group(0) for gr in groups]
    num_group = regex.group
    if isinstance(num_group, list):
        if not num_group:
            return matches
        return [matches[ind] for ind in num_group]

    try:
        return matches[num_group]
    except IndexError:
        return None


@safe
def apply_regex(  # noqa: WPS212, WPS234
    value_to_match: Optional[AnyType],
    regex: Regex,
) -> Union[List[AnyType], AnyType, None]:
    r"""Match value by a certain regex pattern.

    :param value_to_match: The value to match
    :type value_to_match: AnyType

    :param regex: :term: `matching` object which has parameters for
        regex match
    :type regex: Regex

    :return: Success/Failure container
    :rtype: AnyType

    Example
        >>> apply_regex(
        ...     'abcdef',
        ...     Regex(**{'expression': '(?<=abc)def'})
        ... ).unwrap()
        'def'
        >>> apply_regex(
        ...     'Isaac Newton, physicist',
        ...     Regex(**{'expression': r'(\w+)', 'group': 1}),
        ... ).unwrap()
        'Newton'
        >>> apply_regex(
        ...     'Isaac Newton, physicist',
        ...     Regex(**{'expression': r'(\w+)', 'group': [1, 2]}),
        ... ).unwrap()
        ['Newton', 'physicist']
        >>> apply_regex(None, Regex(**{'expression': 'a+'})).unwrap()
        >>> apply_regex('Open-source matters', None).unwrap()
        'Open-source matters'
    """
    if value_to_match is None:
        return value_to_match

    if not regex or not regex.expression:
        return value_to_match

    pattern = regex.expression
    groups = re.finditer(pattern, value_to_match)
    matches: list = [gr.group(0) for gr in groups]
    num_group: Union[int, List[int]] = regex.group
    if isinstance(num_group, list):
        if not num_group:
            return matches
        return [matches[ind] for ind in num_group]  # typing: ignore
    return matches[num_group]


def apply_casting(
    value_to_cast: AnyType,
    casting: Casting,
) -> Union[AnyType, None]:
    """Casting one type of code to another.

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
    function = unsafe_get_casting_function(casting.to)

    casted_value = function(value_to_cast, casting.original_format)

    if is_successful(casted_value):
        return casted_value
    # add if require_success reraise
    raise casted_value.failure()
