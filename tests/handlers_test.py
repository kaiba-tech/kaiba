# -*- coding: utf-8 -*-

"""Test mapping flow functions."""
import decimal

from returns.pipeline import is_successful

from mapmallow.configuration_schemas import ConfigAttribute, ConfigMapping
from mapmallow.handlers import HandleAttribute, HandleMapping
from mapmallow.schema import ApplySchema


class TestHandleMappings(object):
    """Test HandleMappings function."""

    _apply_schema = ApplySchema(ConfigMapping())
    _handle_mapping = HandleMapping()

    def test(self):
        """Test that we can fetch key in dict."""
        config = {'path': ['key']}
        input_data = {'key': 'val1'}
        assert is_successful(self._apply_schema(config))
        assert self._handle_mapping(
            input_data,
            self._apply_schema(config).unwrap(),
        ).unwrap() == 'val1'

    def test_ifs_value(self):
        """Test that we get a default value if no path and no ifs."""
        config = {
            'path': [],
            'if_statements': [
                {
                    'condition': 'is',
                    'target': 'test',
                    'then': 'if',
                },
            ],
            'default': 'default',
        }
        input_data = {'key': 'val1'}
        assert is_successful(self._apply_schema(config))
        assert self._handle_mapping(
            input_data,
            self._apply_schema(config).unwrap(),
        ).unwrap() == 'default'

    def test_default_value(self):
        """Test that we get a default value if no path and no ifs."""
        config = {
            'path': [],
            'default': 'default',
        }
        input_data = {'key': 'val1'}
        assert is_successful(self._apply_schema(config))
        assert self._handle_mapping(
            input_data,
            self._apply_schema(config).unwrap(),
        ).unwrap() == 'default'


class TestHandleMappingRaises(object):
    """Test HandleMappings function for errors."""

    _run = HandleMapping()
    _apply_schema = ApplySchema(ConfigMapping())

    def test_no_mapping_data_raises(self):
        """Test that we get a default value if no path and no ifs."""


class TestHandleAttribute(object):
    """Test HandleAttribute function."""

    _run = HandleAttribute()
    _apply_schema = ApplySchema(ConfigAttribute())

    def test(self):
        """Test that we can fetch key in dict."""
        input_data = {'key': 'val1'}
        config = {
            'name': 'attrib',
            'mappings': [
                {
                    'path': ['key'],
                },
            ],
        }
        assert is_successful(self._apply_schema(config))
        assert self._run(
            input_data,
            self._apply_schema(config).unwrap(),
        ).unwrap() == 'val1'

    def test_casting_to_decimal(self):
        """Test that we can cast a string value to decimal."""
        config = {
            'name': 'attrib',
            'mappings': [
                {
                    'path': ['key'],
                },
            ],
            'casting': {
                'to': 'decimal',
            },
        }
        input_data = {'key': '1,123,123.12'}

        assert is_successful(self._apply_schema(config))
        assert self._run(
            input_data,
            self._apply_schema(config).unwrap(),
        ).unwrap() == decimal.Decimal('1123123.12')

    def test_all(self):
        """Test that we can fetch key in dict."""
        config = {
            'name': 'attrib',
            'mappings': [
                {
                    'path': ['key'],
                    'if_statements': [
                        {
                            'condition': 'is',
                            'target': 'val1',
                            'then': None,
                        },
                    ],
                    'default': 'default',
                },
                {
                    'path': ['key2'],
                    'if_statements': [
                        {
                            'condition': 'is',
                            'target': 'val2',
                            'then': 'if',
                        },
                    ],
                },
            ],
            'separator': '-',
            'if_statements': [
                {
                    'condition': 'is',
                    'target': 'default-if',
                    'then': None,
                },
            ],
            'default': 'default2',
        }
        input_data = {'key': 'val1', 'key2': 'val2'}
        assert is_successful(self._apply_schema(config))
        assert self._run(
            input_data,
            self._apply_schema(config).unwrap(),
        ).unwrap() == 'default2'
