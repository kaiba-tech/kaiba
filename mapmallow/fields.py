# -*- coding: utf-8 -*-

"""Collection of iso standard fields."""

from marshmallow import fields
from returns.primitives.exceptions import UnwrapFailedError

from mapmallow.constants import (
    ALPHA_THREE,
    ALPHA_TWO,
    INVALID,
    NAME,
    NUMERIC,
    OFFICIAL_NAME,
)
from mapmallow.iso import GetCountryCode, GetCurrencyCode, GetLanguageCode


class CountryCode(fields.String):
    """ISO 3166-1 CountryCode field."""

    _get_code = GetCountryCode()
    _output_formats = [
        ALPHA_TWO,
        ALPHA_THREE,
        NAME,
        NUMERIC,
        OFFICIAL_NAME,
    ]

    default_error_messages = {
        INVALID: 'Please provide a valid iso 3166-1 country code.',
    }

    def __init__(self, output_format=ALPHA_TWO, **kwargs):
        """Make standard output format alpha3.

        supported output formats: 'name', 'numeric', 'alpha3'(default)
        """
        super().__init__(**kwargs)
        if output_format not in self._output_formats:
            raise ValueError(
                'invalid output format {0}, must be one of [{1}]'.format(
                    output_format, ', '.join(self._output_formats),
                ),
            )

        self.output_format = output_format

    def _serialize(self, loaded_value, _attr, _object, **kwargs):
        """Serialize CountryCode object into the given format."""
        if loaded_value is None:
            return None

        return loaded_value[self.output_format]

    def _deserialize(self, country_code, _attr, _data_dict, **kwargs):
        """Deserialize a string into a CountryCode object."""
        if not country_code:  # falsy values are invalid
            raise self.make_error(INVALID)
        try:
            return self._get_code(country_code).unwrap()
        except (UnwrapFailedError, AttributeError, TypeError, ValueError):
            raise self.make_error(INVALID)


class CurrencyCode(fields.String):
    """ISO 4217 CurrencyCode field for Aptic."""

    _get_code = GetCurrencyCode()
    _output_formats = [ALPHA_THREE, NAME, NUMERIC]

    default_error_messages = {
        INVALID: 'Please provide a valid iso 4217 currency code.',
    }

    def __init__(self, output_format=ALPHA_THREE, **kwargs):
        """Make standard output format alpha3.

        supported output formats: 'name', 'numeric', 'alpha3'(default)
        """
        super().__init__(**kwargs)
        if output_format not in self._output_formats:
            raise ValueError(
                'invalid output format {0}, must be one of [{1}]'.format(
                    output_format, ', '.join(self._output_formats),
                ),
            )
        self.output_format = output_format

    def _serialize(self, currency_obj, _attr, _object, **kwargs):
        """Serialize CurrencyCode object into the given format."""
        if currency_obj is None:
            return None
        return currency_obj[self.output_format]

    def _deserialize(self, currency_code, _attr, _data_dict, **kwargs):
        """Deserialize a string into a CurrencyCode object."""
        if not currency_code:  # falsy values are invalid
            raise self.make_error(INVALID)
        try:
            return self._get_code(currency_code).unwrap()
        except (UnwrapFailedError, AttributeError, TypeError, ValueError):
            raise self.make_error(INVALID)


class LanguageCode(fields.String):
    """ISO 639 LanguageCode field for Aptic."""

    _get_code = GetLanguageCode()
    _output_formats = [ALPHA_TWO, ALPHA_THREE, NAME]

    default_error_messages = {
        INVALID: 'Please provide a valid iso 639-3 language code.',
    }

    def __init__(self, output_format=ALPHA_THREE, **kwargs):
        """Make standard output format alpha3.

        supported output formats: 'name', 'alpha_2', 'alpha_3'(default)
        """
        super().__init__(**kwargs)
        if output_format not in self._output_formats:
            raise ValueError(
                'invalid output format {0}, must be one of [{1}]'.format(
                    output_format, ', '.join(self._output_formats),
                ),
            )
        self.output_format = output_format

    def _serialize(self, language_obj, _attr, _object, **kwargs):
        """Serialize Languagecode object into the given format."""
        if language_obj is None:
            return None

        return language_obj[self.output_format]

    def _deserialize(self, language_code, _attr, _data_dict, **kwargs):
        """Deserialize a string into a LanguageCode object."""
        if not language_code:  # falsy values are invalid
            raise self.make_error(INVALID)
        try:
            return self._get_code(language_code).unwrap()
        except (UnwrapFailedError, AttributeError, TypeError, ValueError):
            raise self.make_error(INVALID)


class ZipCode(fields.String):
    """Zip code field for marshmallow schemas."""

    default_error_messages = {
        INVALID: 'Unable to parse or output zipcode.',
    }

    def __init__(
        self,
        country_code='countrycode',
        **kwargs,
    ):
        """Field for ZipCodes.

        Sometimes we need to do some formatting on the zip codes.
        implement that here.

        Norwegian zip codes should be left zero padded up to len = 4
        """
        self.country_code = country_code
        super().__init__(**kwargs)

    def _serialize(self, zip_code, _, schema):
        """Serialize ZipCode depending on country code."""
        if zip_code is None:
            return None
        try:
            if self.country_code in schema and schema[self.country_code]:
                if schema[self.country_code]['alpha_3'] == 'NOR':
                    return zip_code.zfill(4)

        except AttributeError:
            raise self.make_error(INVALID)
        return zip_code

    def _deserialize(self, zip_code, _attr, _data_dict, **kwargs):
        """Deserialize a string into a LanguageCode object."""
        if not zip_code:  # falsy zip_codes are invalid
            raise self.make_error(INVALID)
        try:
            return str(zip_code)
        except (AttributeError, TypeError, ValueError):
            raise self.make_error(INVALID)
