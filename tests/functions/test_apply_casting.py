from returns.pipeline import is_successful

from kaiba.functions import apply_casting
from kaiba.pydantic_schema import Casting


def test_value_but_cast_to_fails():
    """No value should just fail with ValueError."""
    test = apply_casting(None, Casting(**{'to': 'integer'}))
    assert not is_successful(test)
    assert isinstance(test.failure(), ValueError)
    assert 'value_to_cast is empty' in str(test.failure())


def test_string_fails_when_month_is_not_integer():
    """Test threws ValueError when month out of range."""
    test = apply_casting(
        '19.MM.12',
        Casting(**{
            'to': 'date',
            'original_format': 'yy.mm.dd',
        }),
    )
    expected = '{0}{1}'.format(
        'Unable to cast (19.MM.12) to ISO date. ',
        "Exc(invalid literal for int() with base 10: '.M')",
    )
    assert not is_successful(test)
    assert isinstance(test.failure(), ValueError)
    assert str(test.failure()) == expected
