import pytest

from kaiba.collection_handlers import fetch_list_by_keys


def test():
    """Test that we can fetch key in dict."""
    assert fetch_list_by_keys(
        {'key': ['val1']},
        ['key'],
    ) == ['val1']


def test_no_path_raises_value_error():
    """Test that we get an error when we dont send a path."""
    with pytest.raises(ValueError) as ve:
        fetch_list_by_keys(
            {'key': 'val1'},
            [],
        )

    assert 'path list empty' in str(ve.value)  # noqa: WPS441


def test_that_found_value_must_be_list():
    """Test that the value we find must be a list, expect error."""
    with pytest.raises(ValueError) as ve:
        fetch_list_by_keys(
            {'key': 'val1'},
            ['key'],
        )

    assert 'Non list data found' in str(ve.value)
