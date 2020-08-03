# -*- coding: utf-8 -*-

"""Test mapping configuration schema."""
import json

import pytest
from returns.pipeline import is_successful

from mapmallow.configuration_schemas import (
    ConfigAttribute,
    ConfigCasting,
    ConfigIfStatement,
    ConfigMapping,
    ConfigObject,
)
from mapmallow.schema import ApplySchema

_input_data: dict = {}
with open('tests/example.json', 'r') as file_object:
    _input_data = json.loads(file_object.read())


class TestIfStatement(object):
    """Test that if statement config object does what we want."""

    _apply = ApplySchema(ConfigIfStatement())

    @pytest.mark.parametrize('condition', ['is', 'not', 'contains'])
    def test_all_valid_conditions_ok(self, condition):
        """Test that all valid conditions are supported."""
        test = {'condition': condition, 'target': 'test', 'then': 'value'}
        assert is_successful(self._apply(test))

    def test_invalid_condition_fails(self):
        """Test that invalid condition raises error."""
        test = {'condition': 'bad', 'target': 'test', 'then': 'value'}
        assert not is_successful(self._apply(test))

    def test_that_target_can_be_none(self):
        """Test that target can be None."""
        test = {'condition': 'is', 'target': None, 'then': 'value'}
        assert is_successful(self._apply(test))

    def test_that_then_can_be_none(self):
        """Test that then can be None."""
        test = {'condition': 'is', 'target': 'target', 'then': None}
        assert is_successful(self._apply(test))


class TestCasting(object):
    """Test that casting schema does what we want."""

    _apply = ApplySchema(ConfigCasting())

    @pytest.mark.parametrize('to', ['integer', 'decimal'])
    def test_only_to_validate(self, to):
        """Giving only 'to' should be okay."""
        test = {'to': to}
        assert is_successful(self._apply(test))

    def test_bad_to_values_should_fail(self):
        """Dont let unsupported cast to values validate."""
        test = {'to': 'rainbow'}
        assert not is_successful(self._apply(test))

    @pytest.mark.parametrize(
        'o_format', ['integer_containing_decimals', 'decimal'],
    )
    def test_only_supported_formats(self, o_format):
        """Test that supported original formats validates ok."""
        test = {'to': 'integer', 'original_format': o_format}
        assert is_successful(self._apply(test))

    def test_only_original_format_fails(self):
        """Giving only original format should fail."""
        test = {'original_format': 'decimal'}
        assert not is_successful(self._apply(test))

    def bad_original_format_fails(self):
        """Don't let bad original format values validate."""
        test = {'to': 'integer', 'original_format': 'rainbow'}
        assert not is_successful(self._apply(test))

    @pytest.mark.parametrize(
        'original_format', [
            'yymmdd',
            'yy-mm-dd',
            'yyyymmdd',
            'yyyy-mm-dd',
            'ddmmyy',
            'dd-mm-yy',
            'ddmmyyyy',
            'dd-mm-yyyy',
            'mmddyy',
            'mm-dd-yy',
            'mmddyyyy',
            'mm-dd-yyyy',
        ],
    )
    def test_date_with_original_format_validates(self, original_format):
        """Test that date with original format validates."""
        test = {'to': 'date', 'original_format': original_format}
        assert is_successful(self._apply(test))

    @pytest.mark.parametrize(
        'original_format', [
            'yyammdd',
            'yy0mm0dd',
            'yymmmdd',
            'test-string',
        ],
    )
    def test_fail_with_invalid_original_format(self, original_format):
        """Test that config fails if original format for date is invalid."""
        test = {'to': 'date', 'original_format': original_format}
        assert not is_successful(self._apply(test))

    def test_fail_with_missing_original_format(self):
        """Test that we get good error message when not providing format."""
        test = {'to': 'date'}
        assert str(
            self._apply(test).failure(),
        ) == "{'_schema': ['original_format requried when to equals date']}"


class TestMapping(object):
    """Test that mapping schema does what we want."""

    _apply = ApplySchema(ConfigMapping())

    def test_ok(self):
        """Test that okay config is ok."""
        test = {'path': ['test', 'path'], 'default': 'def'}
        assert is_successful(self._apply(test))

    def test_path_or_default_required_path(self):
        """Test that only path is ok."""
        test = {'path': ['test']}
        assert is_successful(self._apply(test))

    def test_path_or_default_required_default(self):
        """Test that only default is ok."""
        test = {'default': 'bob'}
        assert is_successful(self._apply(test))

    def test_path_or_default_required_none_fails(self):
        """Test that if not path or default provided it fails."""
        test = {'if_statements': 'test'}
        assert not is_successful(self._apply(test))


class TestConfigAttribute(object):
    """Test validation of ConfigAttribute."""

    _apply = ApplySchema(ConfigAttribute())

    def test_mappings_or_default_is_enough_mappings(self):
        """Test that only mappings is okay."""
        test = {
            'name': 'attribute',
            'mappings': [
                {
                    'default': 'val',
                },
            ],
        }
        assert is_successful(self._apply(test))

    def test_mappings_or_default_is_enough_default(self):
        """Test that only a default value is okay."""
        test = {
            'name': 'attribute',
            'default': 'def',
        }
        assert is_successful(self._apply(test))

    def test_mappings_or_default_is_enough_none(self):
        """Test that no mappings or default fails."""
        test = {
            'name': 'attribute',
        }
        assert not is_successful(self._apply(test))


class TestConfigObject(object):
    """Test validation of ConfigObject."""

    _apply = ApplySchema(ConfigObject())

    _base_attribute = {
        'name': 'attribute',
        'mappings': [
            {
                'default': 'val',
            },
        ],
    }

    def test_iterate_true_required_path_to_iterable(self):
        """When iterate is true, path to iterable is required ok."""
        test = {
            'name': 'obj',
            'array': True,
            'iterate': True,
            'path_to_iterable': ['test'],
            'attributes': [self._base_attribute],
        }
        assert is_successful(self._apply(test))

    def test_no_path_to_iterable_fails(self):
        """When iterate is true, path to iterable is required fails."""
        test = {
            'name': 'obj',
            'array': True,
            'iterate': True,
            'attributes': [self._base_attribute],
        }
        assert not is_successful(self._apply(test))


class TestLoadingConfigurationFile(object):
    """Test Validation(Load) and Output(Dump) of aptic model."""

    _apply = ApplySchema(ConfigObject())

    def test(self):
        """Test that we can fetch key in dict."""
        dumped = self._apply(_input_data['root'])
        assert is_successful(dumped)
        #  add assert json.dumps(dumped) == self._result_data
