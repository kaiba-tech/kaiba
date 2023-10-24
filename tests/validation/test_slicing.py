import pytest
from pydantic import ValidationError

from kaiba.models.slicing import Slicing


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = Slicing(**{'from': 0})
    assert test.slice_from == 0
    assert test.slice_to is None


def test_invalid():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        # Ignore type on purpose since we want to check error
        Slicing(to=0)  # type: ignore 

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('from',)
    assert errors['msg'] == 'Field required'


def test_invalid_type():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        Slicing(**{'from': 'test'})

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('from',)
    assert errors['msg'] == 'Input should be a valid integer'
