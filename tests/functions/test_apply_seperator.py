import pytest

from kaiba.functions import apply_separator


def test_separator():
    """Test separator is applied between two values."""
    test = [['val1', 'val2'], '-']
    assert apply_separator(*test) == 'val1-val2'


def test_separator_one_value():
    """Test when theres only one value, no separator should be applied."""
    test = [['val1'], '-']
    assert apply_separator(*test) == 'val1'


def test_one_integer_value_not_stringified():
    """One value should allways return just the value uncasted."""
    test = [[1], '']
    assert apply_separator(*test) == 1


def test_one_integer_value_with_other_value():
    """Two values no matter the type should be cast to string."""
    assert apply_separator([1, 'val2'], '-') == '1-val2'


def test_no_value():
    """When no value is given we should return None."""
    assert apply_separator([], '-') is None
