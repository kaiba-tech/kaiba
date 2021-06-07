import pytest
from pydantic import ValidationError

from kaiba.pydantic_schema import Slicing


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = Slicing(**{'from': 0})
    assert test.slice_from == 0
    assert test.slice_to is None


def test_invalid():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        Slicing(to=0)

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('from',)
    assert errors['msg'] == 'field required'


def test_invalid_type():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        Slicing(**{'from': 'test'})

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('from',)
    assert errors['msg'] == 'value is not a valid integer'
