from returns.pipeline import is_successful
from typing_extensions import Final

from kaiba.casting._cast_to_integer import cast_to_integer

target: Final[int] = 123


def test_cast_string():
    """Cast a string with numbers to integer."""
    assert cast_to_integer('123').unwrap() == target


def test_cast_negative_string():
    """Cast string with negative number to integer."""
    assert cast_to_integer('-123').unwrap() == -target


def test_cast_decimal_string():
    """Cast a decimal string to integer."""
    assert cast_to_integer(
        '123.0',
        'decimal',
    ).unwrap() == target


def test_cast_negative_decimal_string():
    """Cast a negative decimal string to integer."""
    assert cast_to_integer(
        '-123.0', 'decimal',
    ).unwrap() == -target


def test_cast_decimal_string_rounds_up():
    """Cast a decimal string >= .5 should round up."""
    assert cast_to_integer(
        '122.5',
        'decimal',
    ).unwrap() == target


def test_once_more_cast_decimal_string_rounds_up():
    """Cast a decimal string >= .5 should round up."""
    assert cast_to_integer(
        '123.5',
        'decimal',
    ).unwrap() == 124


def test_cast_decimal_string_rounds_down():
    """Cast a decimal string < .0 should round down."""
    assert cast_to_integer(
        '123.49',
        'decimal',
    ).unwrap() == target


def test_abc_fails():
    """Test that string with letters in fails."""
    test = cast_to_integer('abc')
    assert not is_successful(test)
    assert isinstance(test.failure(), ValueError)
    assert 'Illegal characters in value' in str(test.failure())


def test_abc_with_decimal_argument_fails():
    """Test that string with letters in fails when we supply 'decimal'."""
    test = cast_to_integer(
        'abc',
        'decimal',
    )
    assert not is_successful(test)
    assert isinstance(test.failure(), ValueError)
    assert 'Illegal characters in value' in str(test.failure())
