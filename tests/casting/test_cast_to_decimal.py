from decimal import Decimal

import pytest
from typing_extensions import Final

from kaiba.casting import CastToDecimal

target: Final[Decimal] = Decimal('1234567.89')


def test_string_with_one_period():
    """Test normal decimal value with one period."""
    assert CastToDecimal()(
        '1234567.89',
    ) == target


def test_string_with_one_comma():
    """Test normal decimal value with one comma."""
    assert CastToDecimal()(
        '1234567,89',
    ) == target


def test_string_with_period_and_space():
    """Test space separated decimal number with 1 period."""
    assert CastToDecimal()(
        '1 234 567.89',
    ) == target


def test_string_with_commas_and_period():
    """Test comma as thousands separator with period as decimal."""
    assert CastToDecimal()(
        '1,234,567.89',
    ) == target


def test_string_with_periods_and_comma():
    """Test period as thousands separator with comma as decimal."""
    assert CastToDecimal()(
        '1.234.567,89',
    ) == target


def test_string_with_no_period_nor_comma():
    """Test an integer number will nicely become a decimal."""
    number_string = '123456789'
    test = CastToDecimal()(number_string)
    assert test == Decimal(number_string)


def test_with_integer_containing_decimals_format():
    """Integer_containing_decimals format, should be divided by 100."""
    test = CastToDecimal()(
        '123456789',
        'integer_containing_decimals',
    )
    assert test == target


def test_abc_fails():
    """Test that string with letters in fails."""
    with pytest.raises(ValueError) as ve:
        CastToDecimal()('abc')

    assert str(ve.value) == "Illegal characters in value 'abc'"  # noqa: WPS441


def test_precision_is_maintained():
    """Test high precision decimal value with one period."""
    assert CastToDecimal()(
        '1234567.89123456789',
    ) == Decimal('1234567.89123456789')
