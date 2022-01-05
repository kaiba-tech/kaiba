import decimal

import pytest
from typing_extensions import Final

from kaiba.casting import CastToInteger

target: Final[int] = 123

decimal.getcontext().rounding = decimal.ROUND_HALF_UP


def test_cast_string():
    """Cast a string with numbers to integer."""
    assert CastToInteger()('123') == target


def test_cast_negative_string():
    """Cast string with negative number to integer."""
    assert CastToInteger()('-123') == -target


def test_cast_decimal_string():
    """Cast a decimal string to integer."""
    assert CastToInteger()(
        '123.0',
        'decimal',
    ) == target


def test_cast_negative_decimal_string():
    """Cast a negative decimal string to integer."""
    assert CastToInteger()(
        '-123.0', 'decimal',
    ) == -target


def test_cast_decimal_string_rounds_up():
    """Cast a decimal string >= .5 should round up."""
    assert CastToInteger()(
        '122.5',
        'decimal',
    ) == target


def test_once_more_cast_decimal_string_rounds_up():
    """Cast a decimal string >= .5 should round up."""
    assert CastToInteger()(
        '123.5',
        'decimal',
    ) == 124


def test_cast_decimal_string_rounds_down():
    """Cast a decimal string < .0 should round down."""
    assert CastToInteger()(
        '123.49',
        'decimal',
    ) == target


def test_abc_fails():
    """Test that string with letters in fails."""
    with pytest.raises(ValueError) as ve:
        CastToInteger()('abc')

    assert str(ve.value) == "Illegal characters in value 'abc'"  # noqa: WPS441
