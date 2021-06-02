import pytest
from pydantic import ValidationError

from kaiba.pydantic_schema import KaibaObject


def test_validates_only_object():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = KaibaObject(
        name='Name',
    )
    assert test.name == 'Name'
    assert test.array == False
    assert isinstance(test.iterables, list)
    assert isinstance(test.attributes, list)
    assert isinstance(test.branching_objects, list)
    assert isinstance(test.objects, list)


def test_invalid_only_object():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        KaibaObject(array=False)

    errors = ve.value.errors()[0]  # noqa: WPS441

    assert errors['loc'] == ('name',)
    assert errors['msg'] == 'field required'


def test_validates(valid):
    """Test that we get dict back on valid validation."""
    assert KaibaObject(**valid)


def test_invalid(invalid):
    """Test that we get a list of errors."""
    with pytest.raises(ValidationError) as ve:
        KaibaObject(**invalid)

    errors = ve.value.errors()  # noqa: WPS441

    print(errors)
    assert errors[0]['loc'] == (
        'attributes', 0, 'if_statements', 0, 'condition',
    )
    assert errors[0]['msg'] == 'field required'

    assert errors[1]['loc'] == (
        'branching_objects', 0, 'branching_attributes', 0, 0, 'name',
    )
    assert errors[1]['msg'] == 'field required'
