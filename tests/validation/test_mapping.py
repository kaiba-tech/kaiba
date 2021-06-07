import pytest
from pydantic import ValidationError

from kaiba.pydantic_schema import Mapping


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = Mapping(
        path=['test', 123],
        default='Default',
    )
    assert test.path == ['test', 123]
    assert test.regexp is None
    assert isinstance(test.if_statements, list)
    assert test.default == 'Default'


def test_only_int_and_str_in_path():
    """Test that giving an empty path is an error."""
    with pytest.raises(ValidationError) as ve:
        Mapping(path=[12.2])

    errors = ve.value.errors()[0]  # noqa: WPS441

    assert errors['loc'] == ('path', 0)
    assert errors['msg'] == 'str type expected'
