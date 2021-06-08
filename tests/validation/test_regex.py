import re

import pytest
from pydantic import ValidationError

from kaiba.models.regex import Regex


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = Regex(expression='[1-9]')
    assert test.expression == re.compile('[1-9]')
    assert test.group == 0


def test_invalid_expression():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        Regex(expression='abc[')

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('expression',)
    assert errors['msg'] == 'Invalid regular expression'


def test_invalid_group():
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        Regex(expression='[1-9]', group='test')

    errors = ve.value.errors()[0]  # noqa: WPS441
    assert errors['loc'] == ('group',)
    assert errors['msg'] == 'value is not a valid integer'
