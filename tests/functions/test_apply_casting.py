import pytest

from kaiba.functions import apply_casting
from kaiba.models.casting import Casting


def test_string_fails_when_month_is_not_integer():
    """Test threws ValueError when month out of range."""
    expected = '{0}{1}'.format(
        'Unable to cast (19.MM.12) to ISO date. ',
        "Exc(invalid literal for int() with base 10: '.M')",
    )

    with pytest.raises(ValueError) as ve:
        apply_casting(
            '19.MM.12',
            Casting(**{
                'to': 'date',
                'original_format': 'yy.mm.dd',
            }),
        )

    assert str(ve.value) == expected
