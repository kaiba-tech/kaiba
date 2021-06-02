import pytest
from pydantic import ValidationError

from kaiba.pydantic_schema import IfStatement, ConditionEnum


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = IfStatement(
        condition='is',
        target='test',
        then='then',
    )
    assert test.condition == 'is'
    assert test.target == 'test'
    assert test.then == 'then'
    assert test.otherwise == None


def test_invalid_bad_condition_enum():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        IfStatement(condition='bad', otherwise='otherwise')

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('condition',)
    assert 'not a valid enumeration member' in errors['msg']


def test_invalid_missing_required_fields():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        IfStatement(condition='is')

    errors = ve.value.errors()  # noqa: WPS441

    assert errors[0]['loc'] == ('target',)
    assert errors[0]['msg'] == 'field required'

    assert errors[1]['loc'] == ('then',)
    assert errors[1]['msg'] == 'field required'
