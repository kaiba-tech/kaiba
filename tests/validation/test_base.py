import pytest
from pydantic import ValidationError

from kaiba.models.casting import Casting


def test_invalid():
    """Test that extra attributes are not allowed."""
    with pytest.raises(ValidationError) as ve:
        Casting(to='integer', bob='test')  # type: ignore

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('bob',)
    assert errors['msg'] == 'extra fields not permitted'
