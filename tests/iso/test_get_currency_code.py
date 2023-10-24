import pytest
from returns.primitives.exceptions import UnwrapFailedError

from kaiba.iso import get_currency_code


def test_by_alpha_three_upper():
    """Get currency by alpha 3 code."""
    assert get_currency_code('NOK').unwrap()['alpha_3'] == 'NOK'


def test_by_alpha_three_lower():
    """Get currency by alpha 3 lower cased."""
    assert get_currency_code('nok').unwrap()['alpha_3'] == 'NOK'


def test_by_numeric():
    """Test that we can fetch currency by numeric value."""
    assert get_currency_code('578').unwrap()['alpha_3'] == 'NOK'


def test_by_numeric_int():
    """Test get by numeric with integer."""
    assert get_currency_code(578).unwrap()['alpha_3'] == 'NOK'  # noqa: Z432


def test_by_numeric_below_hundred():
    """Test get by numeric with number < 100."""
    assert get_currency_code('8').unwrap()['alpha_3'] == 'ALL'


def test_by_name():
    """Test getting by name."""
    assert get_currency_code('Norwegian Krone').unwrap()['alpha_3'] == 'NOK'


def test_bad_code():
    """Assert raises with bad name."""
    with pytest.raises(UnwrapFailedError):
        assert get_currency_code('Noway').unwrap()


def test_bad_numeric():
    """Assert raises with bad numeric value."""
    with pytest.raises(UnwrapFailedError):
        assert get_currency_code(123).unwrap()  # noqa: Z432


def test_bad_alpha_two():
    """Assert raises with bad alpha 2 value."""
    with pytest.raises(UnwrapFailedError):
        assert get_currency_code('XX').unwrap()


def test_bad_alpha_three():
    """Assert raises with bad alpha 3 value."""
    with pytest.raises(UnwrapFailedError):
        assert get_currency_code('NAN').unwrap()
