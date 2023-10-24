import pytest
from returns.primitives.exceptions import UnwrapFailedError

from kaiba.functions import apply_separator


def test_separator():
    """Test separator is applied between two values."""
    test: list = [['val1', 'val2'], '-']
    assert apply_separator(*test).unwrap() == 'val1-val2'


def test_separator_one_value():
    """Test when theres only one value, no separator should be applied."""
    test: list = [['val1'], '-']
    assert apply_separator(*test).unwrap() == 'val1'


def test_one_integer_value_not_stringified():
    """One value should allways return just the value uncasted."""
    test: list = [[1], '']
    assert apply_separator(*test).unwrap() == 1


def test_one_integer_value_with_other_value():
    """Two values no matter the type should be cast to string."""
    test: list = [[1, 'val2'], '-']
    assert apply_separator(*test).unwrap() == '1-val2'


def test_no_value():
    """When no value is given we should return Failure."""
    test: list = [[], '-']
    with pytest.raises(UnwrapFailedError):
        apply_separator(*test).unwrap()


def test_no_separator():
    """Test that no separator throws error."""
    test: list = [['val1', 'val2'], None]
    with pytest.raises(UnwrapFailedError):
        apply_separator(*test).unwrap()
