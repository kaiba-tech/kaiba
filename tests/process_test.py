# -*- coding: utf-8 -*-

"""Test process function."""
from decimal import Decimal
from typing import Any

from marshmallow import Schema, fields
from returns.result import safe

from mapmallow.process import Process
from mapmallow.schema import ApplySchema


@safe
def return_data_as_is(the_data: Any) -> Any:
    """Return data as is."""
    return the_data


class Invoice(Schema):
    """Invoice Schema."""

    amount = fields.Decimal(required=True)


class MySchema(Schema):
    """Base schema."""

    invoices = fields.List(fields.Nested(Invoice))


class TestMapObject(object):
    """Test HandleAttribute function."""

    def test(self):
        """Test that we process data."""
        fn = Process(ApplySchema(MySchema()))
        cfg = {
            'name': 'schema',
            'array': False,
            'iterate': False,
            'objects': [
                {
                    'name': 'invoices',
                    'array': True,
                    'iterate': True,
                    'path_to_iterable': ['root', 'invoices'],
                    'attributes': [
                        {
                            'name': 'amount',
                            'mappings': [
                                {
                                    'path': ['invoices', 'amount'],
                                },
                            ],
                            'default': 0,
                        },
                    ],
                },
            ],
        }
        test_data = {
            'root': {
                'invoices': [
                    {
                        'amount': 100.5,
                    },
                ],
            },
        }

        expected_result = {
            'invoices': [{'amount': Decimal('100.5')}],
        }

        assert fn(test_data, cfg).unwrap() == expected_result

    def test_bad_cfg(self):
        """Test that we process data."""
        fn = Process(ApplySchema(MySchema()))
        cfg = {
            'name': 'schema',
            'array': False,
            'iterate': False,
            'objects': [
                {
                    'name': 'invoices',
                    'array': True,
                },
            ],
        }
        test_data: dict = {'root': {}}

        expected = 'Objects, attributes or branching_objects is required'

        assert expected in str(fn(test_data, cfg).failure())
