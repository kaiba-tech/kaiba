import pytest
from typing_extensions import Final

from kaiba.casting import CastToDate

target_after_2000: Final['str'] = '2019-09-07'
target_before_2000: Final['str'] = '1994-06-08'


def test_string_yyyymmdd_no_delimiter():
    """Test that yyyymmdd pattern is accepted."""
    assert CastToDate()(
        '20190907',
        'yyyymmdd',
    ) == target_after_2000


def test_string_ddmmyyyy_no_delimiter():
    """Test that ddmmyyyy pattern is accepted."""
    assert CastToDate()(
        '07092019',
        'ddmmyyyy',
    ) == target_after_2000


def test_string_mmddyyyy_no_delimiter():
    """Test that mmddyyyy pattern is accepted."""
    assert CastToDate()(
        '09072019',
        'mmddyyyy',
    ) == target_after_2000


def test_string_yyyymmdd_with_hyphen():
    """Test that yyyy-mm-dd pattern is accepted."""
    assert CastToDate()(
        '2019-09-07',
        'yyyy-mm-dd',
    ) == target_after_2000


def test_string_yyyymmdd_with_back_slash():
    """Test that yyyy/mm/dd pattern is accepted."""
    assert CastToDate()(
        '2019/09/07',
        'yyyy/mm/dd',
    ) == target_after_2000


def test_string_yyyymmdd_with_dots():
    """Test that yyyy.mm.dd pattern is accepted."""
    assert CastToDate()(
        '2019.09.07',
        'yyyy.mm.dd',
    ) == target_after_2000


def test_string_ddmmyyyy_with_hyphen():
    """Test that dd-mm-yyyy pattern is accepted."""
    assert CastToDate()(
        '07-09-2019',
        'dd-mm-yyyy',
    ) == target_after_2000


def test_string_ddmmmyyyy_with_back_slash():
    """Test that dd/mm/yyyy pattern is accepted."""
    assert CastToDate()(
        '07/09/2019',
        'dd/mm/yyyy',
    ) == target_after_2000


def test_string_ddmmmyyyy_with_dots():
    """Test that dd.mm.yyyy pattern is accepted."""
    assert CastToDate()(
        '07.09.2019',
        'dd.mm.yyyy',
    ) == target_after_2000


def test_string_mmddyyyy_hyphen():
    """Test that mm-dd-yyyy pattern is accepted."""
    assert CastToDate()(
        '09-07-2019',
        'mm-dd-yyyy',
    ) == target_after_2000


def test_string_mmddyyyy_back_slash():
    """Test that mm/dd/yyyy pattern is accepted."""
    assert CastToDate()(
        '09/07/2019',
        'mm/dd/yyyy',
    ) == target_after_2000


def test_string_mmddyyyy_dots():
    """Test that mm.dd.yyyy pattern is accepted."""
    assert CastToDate()(
        '09.07.2019',
        'mm.dd.yyyy',
    ) == target_after_2000


def test_string_mmddyy_no_delimiter_after_2000():
    """Test that mmddyy pattern is accepted."""
    assert CastToDate()(
        '090719',
        'mmddyy',
    ) == target_after_2000


def test_string_mmddyy_no_delimiter_before_2000():
    """Test that mm.dd.yy pattern is accepted."""
    assert CastToDate()(
        '060894',
        'mmddyy',
    ) == target_before_2000


def test_string_yymmdd_no_delimiter_after_2000():
    """Test that yymmdd pattern is accepted."""
    assert CastToDate()(
        '190907',
        'yymmdd',
    ) == target_after_2000


def test_string_yymmdd_no_delimiter_before_2000():
    """Test that yymmdd pattern is accepted."""
    assert CastToDate()(
        '940608',
        'yymmdd',
    ) == target_before_2000


def test_string_ddmmyy_no_delimiter_after_2000():
    """Test that ddmmyy pattern is accepted."""
    assert CastToDate()(
        '070919',
        'ddmmyy',
    ) == target_after_2000


def test_string_ddmmyy_no_delimiter_before_2000():
    """Test that ddmmyy pattern is accepted."""
    assert CastToDate()(
        '080694',
        'ddmmyy',
    ) == target_before_2000


def test_string_mmddyy_with_dots_after_2000():
    """Test that mm.dd.yy pattern is accepted."""
    assert CastToDate()(
        '09.07.19',
        'mm.dd.yy',
    ) == target_after_2000


def test_string_mmddyy_with_dots_before_2000():
    """Test that mm.dd.yy pattern is accepted."""
    assert CastToDate()(
        '06.08.94',
        'mm.dd.yy',
    ) == target_before_2000


def test_string_ddmmyy_with_dots_after_2000():
    """Test that dd.mm.yy pattern is accepted."""
    assert CastToDate()(
        '07.09.19',
        'dd.mm.yy',
    ) == target_after_2000


def test_string_ddmmyy_with_dots_before_2000():
    """Test that dd.mm.yy pattern is accepted."""
    assert CastToDate()(
        '08.06.94',
        'dd.mm.yy',
    ) == target_before_2000


def test_string_yymmdd_with_dots_after_2000():
    """Test that yy.mm.dd pattern is accepted."""
    assert CastToDate()(
        '19.09.07',
        'yy.mm.dd',
    ) == target_after_2000


def test_string_yymmdd_with_dots_before_2000():
    """Test that yy.mm.dd pattern is accepted."""
    assert CastToDate()(
        '94.06.08',
        'yy.mm.dd',
    ) == target_before_2000


def test_string_fails_as_invalid_date():
    """Test threws ValueError when invalid date passed."""
    with pytest.raises(ValueError) as ve:
        CastToDate()(
            '994.06.08',
            'yyy.mm.dd',
        )

    assert 'Error: Casting failed' in str(ve.value)  # noqa: WPS441


def test_string_fails_when_month_out_of_range():
    """Test threws ValueError when month out of range."""
    with pytest.raises(ValueError) as ve:
        CastToDate()(
            '19.14.12',
            'yy.mm.dd',
        )

    assert 'Error: month must be in 1..12' in str(ve.value)  # noqa: WPS441


def test_string_fails_when_month_is_not_integer():
    """Test threws ValueError when month out of range."""
    with pytest.raises(ValueError) as ve:
        CastToDate()(
            '19.MM.12',
            'yy.mm.dd',
        )
    assert "invalid literal for int() with base 10: '.M'" in str(
        ve.value,  # noqa: WPS441
    )
