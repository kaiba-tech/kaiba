import pytest
from pydantic import ValidationError

from kaiba.models.iterator import Iterator


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = Iterator(
        alias='test',
        path=['data'],
    )
    assert test.alias == 'test'
    assert test.path == ['data']


def test_invalid():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        Iterator(**{'alias': 'test'})

    errors = ve.value.errors()[0]  # noqa: WPS441

    assert errors['loc'] == ('path',)
    assert errors['msg'] == 'Field required'


def test_empty_path_is_error():
    """Test that giving an empty path is an error."""
    with pytest.raises(ValidationError) as ve:
        Iterator(alias='test', path=[])

    errors = ve.value.errors()[0]  # noqa: WPS441

    assert errors['loc'] == ('path',)
    assert 'List should have at least 1 item' in errors['msg']


def test_only_int_and_str_in_path():
    """Test that giving an empty path is an error."""
    with pytest.raises(ValidationError) as ve:
        Iterator(alias='test', path=[12.2])

    errors = ve.value.errors()[0]  # noqa: WPS441

    assert errors['loc'] == ('path', 0, 'str')
    assert errors['msg'] == 'Input should be a valid string'
