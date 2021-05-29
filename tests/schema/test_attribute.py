from pydantic import ValidationError
from returns.pipeline import is_successful

from kaiba.pydantic_schema import Attribute


def test_validates():
    """Test that we get dict back on valid validation."""
    test: dict = {'name': 'attrib', 'default': 'bob'}
    try:
        att = Attribute(**test)
    except ValidationError as e:
        print(e.json())

    assert 1 == 2

    assert attribute_validator(test).unwrap() == test
