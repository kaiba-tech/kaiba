# -*- coding: utf-8 -*-

"""Test mapping operation functions."""
import pytest
from marshmallow import Schema, ValidationError

from mapmallow.fields import CountryCode, CurrencyCode, LanguageCode, ZipCode


class TestGetCountryCode(object):
    """Test FetchDataByKeys function."""

    class MySchema(Schema):
        """Testschema."""

        country = CountryCode(  # type: ignore
            output_format='alpha_2',
            allow_none=True,
        )

    def load_and_dump(self, country) -> str:
        """Help function for the tests."""
        return self.MySchema().dump(
            self.MySchema().load({'country': country}),
        )['country']

    def test_by_alpha2(self):
        """Test that we can fetch key in dict."""
        assert self.load_and_dump('NO') == 'NO'

    def test_by_numeric(self):
        """Test that we can fetch currency by numeric value."""
        assert self.load_and_dump('578') == 'NO'

    def test_by_numeric_int(self):
        """Test get by numeric with integer."""
        assert self.load_and_dump(578) == 'NO'  # noqa: Z432

    def test_by_numeric_below_hundred(self):
        """Test get by numeric with number < 100."""
        assert self.load_and_dump('8') == 'AL'

    def test_by_name(self):
        """Test getting by name."""
        assert self.load_and_dump('Norway') == 'NO'

    def test_by_official_name(self):
        """Test getting by official name."""
        assert self.load_and_dump('Kingdom of Norway') == 'NO'

    def test_can_return_none(self):
        """Assert that when allow none is true we can get a None value."""
        assert self.load_and_dump(None) is None


class TestGetCountryCodeRaises(object):
    """Test FetchDataByKeys function."""

    _error_msg_one = 'Please provide a valid iso 3166-1 country code.'
    _error_msg_two = 'Please provide a valid output format'

    class MySchema(Schema):
        """Testschema."""

        country = CountryCode(required=True)  # type: ignore

    def test_bad_country_code(self):
        """Test that we get an load error with a bad country code."""
        with pytest.raises(ValidationError) as err:
            self.MySchema().load({'country': 'bad country'})

        error = err.value.messages  # noqa: WPS441
        assert 'country' in error
        assert error['country'] == [self._error_msg_one]

    def test_falsy_country_code(self):
        """Test that we get an exception when no country code is provided."""
        with pytest.raises(ValidationError) as err:
            self.MySchema().load({'country': ''})
        error = err.value.messages  # noqa: WPS441
        assert 'country' in error
        assert error['country'] == [self._error_msg_one]

    def test_bad_output_format(self):
        """Test that outputting country will fail."""
        with pytest.raises(ValueError):
            class BadSchema(Schema):
                """Bad test schema."""

                country = CountryCode(output_format='test')  # type: ignore


class TestGetCurrencyCode(object):
    """Test FetchDataByKeys function."""

    class MySchema(Schema):
        """Testschema."""

        currency = CurrencyCode(  # type: ignore
            output_format='alpha_3',
            allow_none=True,
        )

    def load_and_dump(self, currency) -> str:
        """Help function for the tests."""
        return self.MySchema().dump(
            self.MySchema().load({'currency': currency}),
        )['currency']

    def test_by_alpha2(self):
        """Test that we can fetch key in dict."""
        assert self.load_and_dump('NOK') == 'NOK'

    def test_by_numeric(self):
        """Test that we can fetch currency by numeric value."""
        assert self.load_and_dump('578') == 'NOK'

    def test_by_numeric_int(self):
        """Test get by numeric with integer."""
        assert self.load_and_dump(578) == 'NOK'  # noqa: Z432

    def test_by_numeric_below_hundred(self):
        """Test get by numeric with number < 100."""
        assert self.load_and_dump('8') == 'ALL'

    def test_by_name(self):
        """Test getting by name."""
        assert self.load_and_dump('Norwegian Krone') == 'NOK'

    def test_can_return_none(self):
        """Assert that when allow none is true we can get a None value."""
        assert self.load_and_dump(None) is None


class TestGetCurrencyCodeRaises(object):
    """Test FetchDataByKeys function."""

    _error_msg_one = 'Please provide a valid iso 4217 currency code.'
    _error_msg_two = 'Please provide a valid output format'

    class MySchema(Schema):
        """Testschema."""

        currency = CurrencyCode(output_format='alpha_3')  # type: ignore

    def test_bad_currency_code(self):
        """Test that we get an load error with a bad currency code."""
        with pytest.raises(ValidationError) as err:
            self.MySchema().load({'currency': 'bad language'})

        error = err.value.messages  # noqa: WPS441
        assert 'currency' in error
        assert error['currency'] == [self._error_msg_one]

    def test_falsy_currency_code(self):
        """Test that we get an exception when no country code is provided."""
        with pytest.raises(ValidationError) as err:
            self.MySchema().load({'currency': ''})
        error = err.value.messages  # noqa: WPS441
        assert 'currency' in error
        assert error['currency'] == [self._error_msg_one]

    def test_bad_output_format(self):
        """Test that outputting country will fail."""
        with pytest.raises(ValueError):
            class BadSchema(Schema):
                """Bad test schema."""

                currency = CurrencyCode(output_format='test')  # type: ignore


class TestGetLanguageCode(object):
    """Test FetchDataByKeys function."""

    class MySchema(Schema):
        """Testschema."""

        language = LanguageCode(  # type: ignore
            output_format='alpha_2',
            allow_none=True,
        )

    def load_and_dump(self, language) -> str:
        """Help function for the tests."""
        return self.MySchema().dump(
            self.MySchema().load({'language': language}),
        )['language']

    def test_by_alpha2(self):
        """Test that we can fetch key in dict."""
        assert self.load_and_dump('NO') == 'NO'

    def test_by_alpha3(self):
        """Test that we can fetch currency by numeric value."""
        assert self.load_and_dump('nor') == 'NO'

    def test_by_name(self):
        """Test getting by name."""
        assert self.load_and_dump('Norwegian') == 'NO'

    def test_can_return_none(self):
        """Assert that when allow none is true we can get a None value."""
        assert self.load_and_dump(None) is None


class TestGetLanguageCodeRaises(object):
    """Test FetchDataByKeys function."""

    _error_msg_one = 'Please provide a valid iso 639-3 language code.'
    _error_msg_two = 'Please provide a valid output format'

    class MySchema(Schema):
        """Testschema."""

        language = LanguageCode(output_format='alpha_2')  # type: ignore

    def test_bad_language_code(self):
        """Test that we get an load error with a bad language code."""
        with pytest.raises(ValidationError) as err:
            self.MySchema().load({'language': 'bad language'})

        error = err.value.messages  # noqa: WPS441
        assert 'language' in error
        assert error['language'] == [self._error_msg_one]

    def test_falsy_language_code(self):
        """Test that we get an exception when no country code is provided."""
        with pytest.raises(ValidationError) as err:
            self.MySchema().load({'language': ''})
        error = err.value.messages  # noqa: WPS441
        assert 'language' in error
        assert error['language'] == [self._error_msg_one]

    def test_bad_output_format(self):
        """Test that outputting country will fail."""
        with pytest.raises(ValueError):
            class BadSchema(Schema):
                """Bad test schema."""

                language = LanguageCode(output_format='test')  # type: ignore


class TestGetZipCode(object):
    """Test FetchDataByKeys function."""

    class MySchema(Schema):
        """Testschema."""

        countrycode = CountryCode()  # type: ignore
        zipcode = ZipCode(allow_none=True)  # type: ignore

    def load_and_dump(self, country, zip_code) -> str:
        """Help function for the tests."""
        return self.MySchema().dump(
            self.MySchema().load(
                {'countrycode': country, 'zipcode': zip_code},
            ),
        )['zipcode']

    def test_by_alpha2(self):
        """Test that we can fetch key in dict."""
        assert self.load_and_dump('NO', '123') == '0123'

    def test_by_alpha3(self):
        """Test that we can fetch currency by numeric value."""
        assert self.load_and_dump('NO', '1234') == '1234'

    def test_by_name(self):
        """Test getting by name."""
        assert self.load_and_dump('DK', '123') == '123'

    def test_can_return_none(self):
        """Assert that when allow none is true we can get a None value."""
        assert self.load_and_dump('NO', None) is None


class TestGetZipCodeRaises(object):
    """Test FetchDataByKeys function."""

    _error_msg_one = 'Unable to parse or output zipcode.'

    class MySchema(Schema):
        """Testschema."""

        countrycode = CountryCode()  # type: ignore
        zipcode = ZipCode(required=True)  # type: ignore

    def test_bad_zip_code(self):
        """Test that we get an load error with a bad language code."""
        with pytest.raises(ValidationError) as err:
            self.MySchema().load({'countrycode': 'NO', 'zipcode': ''})

        error = err.value.messages  # noqa: WPS441
        assert 'zipcode' in error
        assert error['zipcode'] == [self._error_msg_one]
