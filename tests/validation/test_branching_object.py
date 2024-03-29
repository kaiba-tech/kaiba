import pytest
from pydantic import ValidationError

from kaiba.models.branching_object import BranchingObject


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = BranchingObject(
        name='Name',
    )
    assert test.name == 'Name'
    assert test.array is False
    assert isinstance(test.iterators, list)
    assert isinstance(test.branching_attributes, list)


def test_invalid():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        BranchingObject(array=False)  # type: ignore

    errors = ve.value.errors()[0]  # noqa: WPS441

    assert errors['loc'] == ('name',)
    assert errors['msg'] == 'Field required'
