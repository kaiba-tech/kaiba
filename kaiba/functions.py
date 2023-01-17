import re
from decimal import Decimal
from typing import Any, List, Optional, Union

from kaiba.casting import get_casting_function
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
        ...     '1',
        ...     [
        ...         IfStatement(condition='is', target='1', then='2'),
        ...     ],
        ... )
        '2'
        >>> apply_if_statements(
        ...     'a',
        ...     [
        ...         IfStatement(
        ...             condition='is',
        ...             target='1',
        ...             then='2',
        ...             otherwise='3',
        ...         )
        ...     ],
        ... )
        '3'
    """
    for statement in statements:

        if_value = _apply_statement(
            if_value, statement,
        )

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


def apply_separator(
    mapped_values: List[AnyType],
    separator: str,
) -> Union[AnyType, None]:
    """Apply separator between the values of a List[Any].

    :param mapped_values: The list of values to join with the separator
    :type mapped_values: List[AnyType]

    :param separator: :term:`separator` value to join mapped_values list with
    :type separator: str

    :return: Success/Failure containers
    :rtype: AnyType

    Example
        >>> apply_separator(['a', 'b', 'c'], ' ')
        'a b c'
        >>> apply_separator([1, 'b', True], ' ')
        '1 b True'
        >>> apply_separator([], ' ') is None
        True
    """
    if not mapped_values:
        return None

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


def apply_regex(  # noqa: WPS212, WPS234, C901
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
        ... )
        'def'
        >>> apply_regex(
        ...     'Isaac Newton, physicist',
        ...     Regex(**{'expression': r'(\w+)', 'group': 1}),
        ... )
        'Newton'
        >>> apply_regex(
        ...     'Isaac Newton, physicist',
        ...     Regex(**{'expression': r'(\w+)', 'group': [1, 2]}),
        ... )
        ['Newton', 'physicist']
    """
    pattern = regex.expression
    groups = re.finditer(pattern, value_to_match)
    matches = [gr.group(0) for gr in groups]
    num_group = regex.group
    if isinstance(num_group, list):
        if not num_group:
            return matches
        try:
            return [matches[ind] for ind in num_group]
        except IndexError:
            return None
    try:
        return matches[num_group]
    except IndexError:
        return None


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
        >>> apply_casting('123', Casting(**{'to': 'integer'}))
        123
        >>> apply_casting('123.12', Casting(**{'to': 'decimal'}))
        Decimal('123.12')
    """
    function = get_casting_function(casting.to)

    return function(value_to_cast, casting.original_format)
