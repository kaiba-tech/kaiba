from kaiba.functions import apply_separator


def test_separator():
    """Test separator is applied between two values."""
    assert apply_separator(['val1', 'val2'], '-') == 'val1-val2'


def test_separator_one_value():
    """Test when theres only one value, no separator should be applied."""
    assert apply_separator(['val1'], '-') == 'val1'


def test_one_integer_value_not_stringified():
    """One value should allways return just the value uncasted."""
    assert apply_separator([1], '') == 1


def test_one_integer_value_with_other_value():
    """Two values no matter the type should be cast to string."""
    assert apply_separator([1, 'val2'], '-') == '1-val2'


def test_no_value():
    """When no value is given we should return None."""
    assert apply_separator([], '-') is None
