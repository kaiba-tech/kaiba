import pytest
from pydantic import ValidationError

from kaiba.models.if_statement import Conditions, IfStatement


def test_validates():  # noqa: WPS218
    """Test that dict is marshalled to pydantic object."""
    test = IfStatement(
        condition='is',
        target=None,
        then='then',
    )
    assert test.condition == 'is'
    assert test.target is None
    assert test.then == 'then'
    assert test.otherwise is None


def test_invalid_bad_condition_enum():  # noqa: WPS218
    """Test that we get validation error with correct message."""
    with pytest.raises(ValidationError) as ve:
        IfStatement(  # type: ignore
            condition='bad',
            otherwise='otherwise',
        )

    condition = ve.value.errors()[0]  # noqa: WPS441
    assert condition['loc'] == ('condition',)
    msg = condition['msg']
    assert all(con.value in msg for con in Conditions)

    target = ve.value.errors()[1]  # noqa: WPS441
    assert target['loc'] == ('target',)
    assert target['msg'] == 'Field required'

    then = ve.value.errors()[2]  # noqa: WPS441
    assert then['loc'] == ('then',)
    assert then['msg'] == 'Field required'
