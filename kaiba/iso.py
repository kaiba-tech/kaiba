from __future__ import annotations

from pycountry import countries, currencies, languages
from returns.result import safe

from kaiba.constants import ALPHA_THREE, ALPHA_TWO, NAME, NUMERIC, OFFICIAL_NAME


@safe
def get_country_code(code: str | int) -> dict:
    """Find country by code or name."""
    code = str(code).strip()
    country = countries.get(alpha_2=code.upper())
    country = country or countries.get(alpha_3=code.upper())
    country = country or countries.get(numeric=code.zfill(3))
    country = country or countries.get(name=code)
    country = country or countries.get(official_name=code)

    if not country:
        raise ValueError(
            '{message}({country})'.format(
                message='Could not find country matching value',
                country=code,
            ),
        )

    return {
        ALPHA_TWO: country.alpha_2.upper(),
        ALPHA_THREE: country.alpha_3.upper(),
        NAME: country.name,
        NUMERIC: country.numeric,
        OFFICIAL_NAME: _get_official_name(country).value_or(None),
    }


@safe
def _get_official_name(country) -> str:
    return country.official_name


@safe
def get_currency_code(code: str | int) -> dict:
    """Try to create a Currency object."""
    code = str(code).strip()

    currency = currencies.get(alpha_3=code.upper())
    currency = currency or currencies.get(numeric=code.zfill(3))
    currency = currency or currencies.get(name=code)

    if not currency:
        raise ValueError(
            '{message}({code})'.format(
                message='Could not find currency matching code',
                code=code,
            ),
        )

    return {
        ALPHA_THREE: currency.alpha_3.upper(),
        NUMERIC: currency.numeric,
        NAME: currency.name,
    }


@safe
def get_language_code(code: str) -> dict:
    """Try to create a Language object."""
    code = str(code).strip()
    lan = languages.get(alpha_2=code.lower())
    lan = lan or languages.get(alpha_3=code.lower())
    lan = lan or languages.get(name=code)

    if not lan:
        raise ValueError(
            '{message}({code})'.format(
                message='Could not find language matching value',
                code=code,
            ),
        )
    return {
        ALPHA_TWO: lan.alpha_2.upper(),
        ALPHA_THREE: lan.alpha_3.upper(),
        NAME: lan.name,
        'scope': lan.scope,
        'type': lan.type,
    }
