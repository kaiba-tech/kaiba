# -*- coding: utf-8 -*-

"""Test some usecases for errors."""
import copy

from marshmallow import Schema, fields
from returns.pipeline import is_successful

from mapmallow.process import Process
from mapmallow.schema import ApplySchema


class MyInvoice(Schema):
    """Invoice Schema."""

    amount = fields.Decimal(required=True)
    due_date = fields.Date()


class MyCustomer(Schema):
    """Customer Schema."""

    name = fields.String()
    address = fields.String()


class MySchema(Schema):
    """Schema."""

    customer = fields.Nested(MyCustomer)
    invoices = fields.List(fields.Nested(MyInvoice))


class TestBadSchemaErrorMessage(object):
    """Test that we get a good error message when process errors."""

    configuration: dict = {
        'name': 'root',
        'array': False,
        'iterate': False,
        'objects': [
            {
                'name': 'customer',
                'array': False,
                'iterate': False,
                'attributes': [
                    {
                        'name': 'name',
                        'mappings': [{'path': ['customer', 'name']}],
                    },
                    {
                        'name': 'address',
                        'mappings': [{'path': ['customer', 'address']}],
                    },
                ],
            },
            {
                'name': 'invoices',
                'array': True,
                'iterate': True,
                'path_to_iterable': ['invoices'],
                'attributes': [
                    {
                        'name': 'amount',
                        'mappings': [{'path': ['invoices', 'amount']}],
                    },
                    {
                        'name': 'due_date',
                        'mappings': [{'path': ['invoices', 'due_date']}],
                    },
                ],
            },
        ],
    }

    test_data: dict = {
        'customer': {
            'name': 'bob',
            'address': 'road1',
        },
        'invoices': [
            {
                'amount': 123,
                'due_date': '2019-10-10',
            },
        ],
    }

    _run = Process(ApplySchema(MySchema()))

    def test_load_the_thing_works(self):
        """Test taht we can load."""
        assert is_successful(self._run(self.test_data, self.configuration))

    def test_missing_array_in_config(self):
        """Test that we get validation error with correct message.

        Sometimes the configuration is bad. so we should get an error that
        tells us whats bad about it.

        """
        cfg = copy.deepcopy(self.configuration)
        cfg['objects'][0].pop('array')

        processed = self._run(self.test_data, cfg)
        assert not is_successful(processed)
        assert 'array' in processed.failure()['objects'][0]  # type: ignore

    def test_missing_required_data_in_config(self):
        """Test that we get an error message when we have bad mapped data."""
        t_data = dict(self.test_data)
        t_data['invoices'][0].pop('amount')

        processed = self._run(t_data, self.configuration)
        assert not is_successful(processed)
        assert 'amount' in processed.failure()['invoices'][0]  # type: ignore
