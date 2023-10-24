import pytest
from returns.primitives.exceptions import UnwrapFailedError

from kaiba.iso import get_language_code


def test_by_alpha_two():
    """Test that we can fetch key in dict."""
    assert get_language_code('NO').unwrap()['alpha_3'] == 'NOR'


def test_by_alpha_three():
    """Test that we can fetch key in dict."""
    assert get_language_code('NOR').unwrap()['alpha_3'] == 'NOR'


def test_by_name():
    """Test getting by name."""
    assert get_language_code('Norwegian').unwrap()['alpha_3'] == 'NOR'


def test_bad_code():
    """Assert raises with bad name."""
    with pytest.raises(UnwrapFailedError):
        assert get_language_code('somelanguage').unwrap()


def test_bad_alpha_two():
    """Assert raises with bad alpha 2 value."""
    with pytest.raises(UnwrapFailedError):
        assert get_language_code('XX').unwrap()


def test_bad_alpha_three():
    """Assert raises with bad alpha 3 value."""
    with pytest.raises(UnwrapFailedError):
        assert get_language_code('XXX').unwrap()
