import datetime
import re

from returns.pipeline import flow
from returns.pointfree import alt, bind, lash
from returns.result import Failure, ResultE, safe
from typing_extensions import Final

from kaiba.models.base import AnyType

_yymmdd_pattern: Final = re.compile(r'^yy[^\w]?mm[^\w]?dd$')
_ddmmyy_pattern: Final = re.compile(r'^dd[^\w]?mm[^\w]?yy$')
_mmddyy_pattern: Final = re.compile(r'^mm[^\w]?dd[^\w]?yy$')

_mmddyyyy_pattern: Final = re.compile(r'^mm[^\w]?dd[^\w]?yyyy$')
_ddmmyyyy_pattern: Final = re.compile(r'^dd[^\w]?mm[^\w]?yyyy$')
_yyyymmdd_pattern: Final = re.compile(r'^yyyy[^\w]?mm[^\w]?dd$')
_iso_pattern: Final = re.compile(r'^\d{4}-\d{2}-\d{2}')

_error_message: Final = 'Unable to cast ({value}) to ISO date. Exc({failure})'


def cast_to_date(
    value_to_cast: AnyType,
    original_format: str,
) -> ResultE[str]:
    r"""
    purpose: Convert string date into ISO format date.

    :input value_to_cast: the string to be converted to a date
    :input original_format: a string describing the format the data string
                            is before convertion.
    :raises ValueError:  when not able to convert or value_to_cast
                            does not match original_format.
    regex_tips  ^ = start of string
                $ = end of string
                [^[0-9]] = matches anything not [0-9]
                [^\d] = matches anything not digits
                \d = matches digits
                {n} = matches previous match n amount of times
                () = grouper, groups up stuff for use in replace.
    """
    date_value = str(value_to_cast)
    return flow(
        date_value,
        _value_is_iso,
        lash(  # type: ignore
            lambda _: _cast_with_millennia(
                date_value,
                original_format=original_format,
            ),
        ),
        lash(  # type: ignore
            lambda _: _cast_with_no_millennia(
                date_value,
                original_format=original_format,
            ),
        ),
        bind(_validate_date),
        alt(  # type: ignore
            lambda failure: ValueError(
                _error_message.format(
                    value=date_value,
                    failure=failure,
                ),
            ),
        ),
    )


@safe
def _value_is_iso(value_to_cast: str) -> str:
    if _iso_pattern.match(value_to_cast):
        return value_to_cast
    raise ValueError('Unable to cast to ISO date')


def _cast_with_millennia(
    value_to_cast: str,
    original_format: str,
) -> ResultE[str]:
    # mm[.]dd[.]yyyy any separator
    if _mmddyyyy_pattern.match(original_format):
        return _apply_regex_sub(
            r'(\d{2})[^\w]?(\d{2})[^\w]?(\d{4})',
            r'\3-\1-\2',
            value_to_cast,
        )

    # dd[.]mm[.]yyyy any separator
    if _ddmmyyyy_pattern.match(original_format):
        return _apply_regex_sub(
            r'(\d{2})[^\w]?(\d{2})[^\w]?(\d{4})',
            r'\3-\2-\1',
            value_to_cast,
        )

    # yyyy[.]mm[.]dd any separator
    if _yyyymmdd_pattern.match(original_format):
        return _apply_regex_sub(
            r'(\d{4})[^\w]?(\d{2})[^\w]?(\d{2})',
            r'\1-\2-\3',
            value_to_cast,
        )

    return Failure(
        ValueError(
            'Unable to case to milennia format: {value}'.format(
                value=value_to_cast,
            ),
        ),
    )


def _cast_with_no_millennia(
    value_to_cast: str,
    original_format: str,
) -> ResultE[str]:
    no_millenia_patterns = {
        _yymmdd_pattern: (
            r'(\d{2})[^\w]?(\d{2})[^\w]?(\d{2})',
            r'\3\2\1',
        ),
        _ddmmyy_pattern: (
            r'(\d{2})[^\w]?(\d{2})[^\w]?(\d{2})',
            r'\1\2\3',
        ),
        _mmddyy_pattern: (
            r'(\d{2})[^\w]?(\d{2})[^\w]?(\d{2})',
            r'\2\1\3',
        ),
    }
    for no_millenia_pattern in no_millenia_patterns:  # noqa: WPS528
        if no_millenia_pattern.match(original_format):
            pattern, arrangement = no_millenia_patterns[no_millenia_pattern]
            return _apply_regex_sub(
                pattern, arrangement, value_to_cast,
            ).bind(
                _convert_ddmmyy_to_iso_date,
            )

    return Failure(
        ValueError(
            'Unable to cast to no millennia format: {value}'.format(
                value=value_to_cast,
            ),
        ),
    )


@safe
def _validate_date(date_string: str) -> str:
    return datetime.date(
        *map(
            int,
            date_string.split('-'),
        ),
    ).isoformat()


@safe
def _apply_regex_sub(
    pattern: str,
    arrangement: str,
    input_string: str,
) -> str:
    return re.sub(pattern, arrangement, input_string)


@safe  # noqa: WPS210, Hard to reduce variables
def _convert_ddmmyy_to_iso_date(  # noqa: WPS210
    date_string: str,
) -> str:

    in_day = int(date_string[:2])
    in_month = int(date_string[2:4])
    in_year = int(date_string[4:6])

    today = datetime.date.today()
    # think of this 'century' variable as century - 1. as in:
    # 2018 = 2000, 1990 = 1900
    century = (today.year // 100) * 100
    # yy = last two digits of year. 2018 = 18, 1990 = 90
    yy = today.year % 100
    if in_year > yy:
        century -= 100
    year = century + in_year
    date_obj = datetime.date(year, in_month, in_day)

    return date_obj.isoformat()
