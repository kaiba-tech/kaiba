# -*- coding: utf-8 -*-

"""Test mapping flow functions."""
from mapmallow.configuration_schemas import ConfigObject
from mapmallow.mapper import Map
from mapmallow.schema import ApplySchema


class TestMapObject(object):
    """Test HandleAttribute function."""

    _map = Map()
    _apply_schema = ApplySchema(ConfigObject())

    def test(self):
        """Test that we can fetch key in dict."""
        config = {
            'name': 'root',
            'array': False,
            'iterate': False,
            'attributes': [
                {
                    'name': 'name',
                    'mappings': [
                        {
                            'path': ['key'],
                        },
                    ],
                },
            ],
        }
        input_data = {'key': 'test name'}
        assert self._map(
            input_data,
            self._apply_schema(config).unwrap(),
        ).unwrap() == {'name': 'test name'}

    def test_array_true_but_no_loop_gives_array(self):
        """Test that we get an array if we set array = true in object."""
        config = {
            'name': 'root',
            'array': True,
            'iterate': False,
            'attributes': [
                {
                    'name': 'name',
                    'mappings': [
                        {
                            'path': ['key'],
                        },
                    ],
                },
            ],
        }
        input_data = {'key': 'test name'}
        assert self._map(
            input_data,
            self._apply_schema(config).unwrap(),
        ).unwrap() == [{'name': 'test name'}]

    def test_double_repeatable(self):
        """Test that we can map nested repeatable objects."""
        config = {
            'name': 'root',
            'array': True,
            'iterate': True,
            'path_to_iterable': ['journals'],
            'attributes': [
                {
                    'name': 'journal_id',
                    'mappings': [{'path': ['journals', 'journal', 'id']}],
                },
            ],
            'objects': [
                {
                    'name': 'invoices',
                    'array': True,
                    'iterate': True,
                    'path_to_iterable': [
                        'journals', 'journal', 'invoices',
                    ],
                    'attributes': [
                        {
                            'name': 'amount',
                            'mappings': [
                                {
                                    'path': [
                                        'invoices', 'amount',
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        }
        input_data = {
            'journals': [
                {
                    'journal': {
                        'id': 1,
                        'invoices': [{'amount': 1.1}, {'amount': 1.2}],
                    },
                },
                {
                    'journal': {
                        'id': 2,
                        'invoices': [{'amount': 1.3}, {'amount': 1.4}],
                    },
                },
            ],
        }
        expected_result = [
            {
                'journal_id': 1,
                'invoices': [
                    {'amount': 1.1},
                    {'amount': 1.2},
                ],
            },
            {
                'journal_id': 2,
                'invoices': [
                    {'amount': 1.3},
                    {'amount': 1.4},
                ],
            },
        ]

        assert self._map(
            input_data,
            self._apply_schema(config).unwrap(),
        ).unwrap() == expected_result

    def test_all(self):
        """Test that we can fetch key in dict."""
        config = {
            'name': 'schema',
            'array': False,
            'iterate': False,
            'attributes': [
                {
                    'name': 'name',
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
                },
            ],
            'objects': [
                {
                    'name': 'address',
                    'array': False,
                    'iterate': False,
                    'attributes': [
                        {
                            'name': 'address1',
                            'mappings': [{'path': ['a1']}],
                        },
                        {
                            'name': 'address2',
                            'mappings': [{'path': ['a2']}],
                        },
                    ],
                },
                {
                    'name': 'people',
                    'array': True,
                    'iterate': True,
                    'path_to_iterable': ['persons'],
                    'attributes': [
                        {
                            'name': 'firstname',
                            'mappings': [{'path': ['persons', 'name']}],
                        },
                    ],
                },
            ],
            'branching_objects': [
                {
                    'name': 'extrafield',
                    'array': True,
                    'iterate': False,
                    'branching_attributes': [
                        [
                            {
                                'name': 'dataname',
                                'default': 'one',
                            },
                            {
                                'name': 'datavalue',
                                'mappings': [
                                    {'path': ['extra', 'extra1']},
                                ],
                            },
                        ],
                        [
                            {
                                'name': 'dataname',
                                'default': 'two',
                            },
                            {
                                'name': 'datavalue',
                                'mappings': [
                                    {'path': ['extra', 'extra2']},
                                ],
                            },
                        ],
                    ],
                },
            ],
        }
        input_data = {
            'key': 'val1',
            'key2': 'val2',
            'a1': 'a1',
            'a2': 'a2',
            'persons': [{'name': 'john'}, {'name': 'bob'}],
            'extra': {
                'extra1': 'extra1val',
                'extra2': 'extra2val',
            },
        }
        expected_result = {
            'name': 'default2',
            'address': {
                'address1': 'a1',
                'address2': 'a2',
            },
            'people': [
                {'firstname': 'john'},
                {'firstname': 'bob'},
            ],
            'extrafield': [
                {'dataname': 'one', 'datavalue': 'extra1val'},
                {'dataname': 'two', 'datavalue': 'extra2val'},
            ],
        }
        assert self._map(
            input_data,
            self._apply_schema(config).unwrap(),
        ).unwrap() == expected_result
