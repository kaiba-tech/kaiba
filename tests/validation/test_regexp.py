import re

import pytest
from pydantic import ValidationError

from kaiba.pydantic_schema import Regexp


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = Regexp(search='[1-9]')
    assert test.search == re.compile('[1-9]')
    assert test.group == 0


def test_invalid_expression():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        Regexp(search='abc[')

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('search',)
    assert errors['msg'] == 'Invalid regular expression'


def test_invalid_group():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        Regexp(search='[1-9]', group='test')

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('group',)
    assert errors['msg'] == 'value is not a valid integer'
