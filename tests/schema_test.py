# -*- coding: utf-8 -*-

"""Test mapping operation functions."""

from marshmallow import Schema, fields, validate
from returns.pipeline import is_successful

from mapmallow.error_handlers import (
    CastToStringUnlessNone,
    CutStringsWhenTooLong,
)
from mapmallow.schema import ApplySchema, MakeConfigurationSkeleton


class NestedSchema(Schema):
    """Person data."""

    name = fields.String(required=True, validate=validate.Length(max=10))
    email = fields.String()


class MainSchema(Schema):
    """Test schema for validating and dumping."""

    people = fields.List(fields.Nested(NestedSchema))


class TestApplySchema(object):
    """Test Validation(Load) and Output(Dump) of aptic model."""

    _get = ApplySchema(MainSchema())

    _input_data: dict = {
        'people': [
            {
                'name': 'bob',
                'email': 'bob@bob.com',
            },
        ],
    }

    def test(self):
        """Test that we can fetch key in dict."""
        dumped = self._get(self._input_data)
        assert is_successful(dumped)
        #  add assert json.dumps(dumped) == self._result_data


class TestApplySchemaBadData(object):
    """Test what we do when we have bad data."""

    _get = ApplySchema(
        MainSchema(many=True),
        {CastToStringUnlessNone(), CutStringsWhenTooLong()},
    )

    _input_data: dict = {
        'people': [
            {
                'name': 'invalidnametoolong',
                'email': 1,
            },
        ],
    }

    def test_bad(self):
        """Test that we get some errors."""
        dumped = self._get([self._input_data])  # type: ignore
        assert is_successful(dumped)


class TestCreateConfigurationSkeleton(object):
    """Test Validation(Load) and Output(Dump) of aptic model."""

    _model = MainSchema
    _create_skeleton = MakeConfigurationSkeleton()

    def test_stuff(self):
        """Test that we can fetch key in dict."""
        test = self._create_skeleton(self._model()).unwrap()
        assert test['name'] == 'root'
        assert test['objects'][0]['name'] == 'people'
        assert len(test['objects'][0]['attributes']) == 2
