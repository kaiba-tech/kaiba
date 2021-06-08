import pytest
from pydantic import ValidationError

from kaiba.models.kaiba_object import KaibaObject


def test_validates_only_object():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = KaibaObject(
        name='Name',
    )
    assert test.name == 'Name'
    assert test.array is False
    assert isinstance(test.iterators, list)
    assert isinstance(test.attributes, list)
    assert isinstance(test.branching_objects, list)
    assert isinstance(test.objects, list)


def test_invalid_only_object():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        KaibaObject(array=False)  # type: ignore

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
        'objects', 0, 'attributes', 0, 'deult'
    )
    assert errors[1]['msg'] == 'extra fields not permitted'

    assert errors[2]['loc'] == (
        'branching_objects', 0, 'branching_attributes', 0, 0, 'name',
    )
    assert errors[2]['msg'] == 'field required'

    # Should also complain about date original format not being correct
