import pytest
from pydantic import ValidationError

from kaiba.pydantic_schema import Attribute


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = Attribute(
        name='Name',
        default='Default',
    )
    assert test.name == 'Name'
    assert test.default == 'Default'
    assert isinstance(test.mappings, list)
    assert isinstance(test.if_statements, list)
    assert test.separator == ''
    assert test.casting is None


def test_invalid():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        Attribute(separator=' ')  # type: ignore

    errors = ve.value.errors()[0]  # noqa: WPS441

    assert errors['loc'] == ('name',)
    assert errors['msg'] == 'field required'
