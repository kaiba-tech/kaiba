import pytest
from returns.primitives.exceptions import UnwrapFailedError

from kaiba.iso import get_country_code

# Norway, NO, NOR, 578
# Albania, AL, ALB, 008


def test():
    """Test that we can fetch key in dict."""
    assert get_country_code('NO').unwrap()['alpha_2'] == 'NO'


def test_no_official_name():
    """Some countries does not have official name.

    We should be able to get these and official_name should be `None`
    """
    assert get_country_code('CA').unwrap()['official_name'] is None


def test_by_numeric():
    """Test that we can fetch currency by numeric value."""
    assert get_country_code('578').unwrap()['numeric'] == '578'


def test_by_numeric_int():
    """Test get by numeric with integer."""
    assert get_country_code(578).unwrap()['numeric'] == '578'  # noqa: Z432


def test_by_numeric_below_hundred():
    """Test get by numeric with number < 100."""
    assert get_country_code('8').unwrap()['numeric'] == '008'


def test_by_name():
    """Test getting by name."""
    assert get_country_code('Norway').unwrap()['name'] == 'Norway'


def test_by_official_name():
    """Test getting by official name."""
    test_value = get_country_code('Kingdom of Norway').unwrap()['official_name']
    assert test_value == 'Kingdom of Norway'


def test_bad_code():
    """Assert raises with bad name."""
    with pytest.raises(UnwrapFailedError):
        assert get_country_code('Noway').unwrap()


def test_bad_numeric():
    """Assert raises with bad numeric value."""
    with pytest.raises(UnwrapFailedError):
        assert get_country_code(123).unwrap()  # noqa: Z432


def test_bad_alpha_two():
    """Assert raises with bad alpha 2 value."""
    with pytest.raises(UnwrapFailedError):
        assert get_country_code('XX').unwrap()


def test_bad_alpha_three():
    """Assert raises with bad alpha 3 value."""
    with pytest.raises(UnwrapFailedError):
        assert get_country_code('XXX').unwrap()
