import pytest
from pydantic import ValidationError

from kaiba.pydantic_schema import Casting, CastingEnum


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = Casting(
        to='integer',
    )
    assert test.to == CastingEnum.INTEGER
    assert test.original_format is None


def test_invalid():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        Casting(to='test')

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('to',)
    assert 'not a valid enumeration member' in errors['msg']
