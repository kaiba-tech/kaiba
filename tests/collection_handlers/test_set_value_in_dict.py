import pytest
from returns.pipeline import is_successful

from kaiba.collection_handlers import set_value_in_dict


def test():
    """Test that we can set value by reference in dict."""
    dictionary = {'key': 'val1'}
    set_value_in_dict('val2', dictionary, ['key'])
    assert dictionary['key'] == 'val2'


def test_multiple_path():
    """Test deeper set value."""
    dictionary = {'key': {'key2': 'val1'}}
    set_value_in_dict('val2', dictionary, ['key', 'key2'])

    assert dictionary['key']['key2'] == 'val2'


def test_no_path_raises_value_error():
    """Test that we get an error when we dont send a path."""
    with pytest.raises(ValueError) as ve:
        set_value_in_dict('val2', {'key': ['val1']}, [])

    assert str(ve.value) == 'path list empty'  # noqa: WPS441


def test_path_to_missing_key_is_ok():
    """Test that missing keys are okay."""
    dictionary: dict = {'key': ['val1']}
    set_value_in_dict('val2', dictionary, ['bob'])
    assert dictionary['bob'] == 'val2'
