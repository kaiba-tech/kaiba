from kaiba.functions import apply_regex
from kaiba.models.regex import Regex


def test_regexp_get_empty_list_grup():
    """Test regexp when group indeces are out of range."""
    regexp = apply_regex(
        'Hard work',
        Regex(**{'expression': 'r', 'group': []}),
    )
    assert regexp.unwrap() == ['r', 'r']


def test_regexp_on_index_out_of_range():
    """Test regexp when group indeces are out of range."""
    regexp = apply_regex(
        'Hard work',
        Regex(**{'expression': 'r', 'group': [1, 2, 3]}),
    )
    assert isinstance(regexp.failure(), IndexError) is True
    assert regexp.failure().args == ('list index out of range',)


def test_no_value_is_ok():
    """When value is None we get a Success(None)."""
    assert apply_regex(None, Regex(**{'expression': 'a'})).unwrap() is None
