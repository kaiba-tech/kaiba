import pytest
from pydantic import ValidationError

from kaiba.models.casting import Casting, CastToOptions


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = Casting(
        to='integer',
    )
    assert test.to == CastToOptions.INTEGER
    assert test.original_format is None


def test_invalid():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        Casting(to='test')

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('to',)
    msg = errors['msg']
    assert all(opt.value in msg for opt in CastToOptions)
