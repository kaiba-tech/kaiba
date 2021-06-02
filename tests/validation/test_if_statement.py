import pytest
from pydantic import ValidationError

from kaiba.pydantic_schema import IfStatement


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = IfStatement(
        condition='is',
    )
    assert test.condition == 'is'
    assert test.target is None
    assert test.then is None
    assert test.otherwise is None


def test_invalid_bad_condition_enum():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        IfStatement(condition='bad', otherwise='otherwise')

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('condition',)
    assert 'not a valid enumeration member' in errors['msg']
