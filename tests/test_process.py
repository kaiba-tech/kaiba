import json

import pytest
from pydantic import ValidationError

from kaiba.process import process_raise


def test_creating_key_to_name():
    """Test that we can fetch key in dict."""
    input_data = {'key': 'test name'}
    config = {
        'name': 'root',
        'array': False,
        'attributes': [
            {
                'name': 'name',
                'data_fetchers': [
                    {
                        'path': ['key'],
                    },
                ],
            },
        ],
    }

    assert process_raise(
        input_data,
        config,
    ) == {'name': 'test name'}


def test_bad_config_gives_failure():
    """Test that we can fetch key in dict."""
    input_data = {'key': 'test name'}
    config = {
        'namme': 'root',
        'attributesadfs': [
            {
                'name': 'name',
                'data_fetchers': [
                    {
                        'path': ['key'],
                    },
                ],
            },
        ],
    }
    with pytest.raises(ValidationError) as ve:
        process_raise(input_data, config)

    assert ve.match('name')  # noqa: WPS441
    assert ve.match('field required')  # noqa: WPS441


def test_array_true_but_no_loop_gives_array():
    """Test that we get an array if we set array = true in object."""
    input_data = {'key': 'test name'}
    config = {
        'name': 'root',
        'array': True,
        'attributes': [
            {
                'name': 'name',
                'data_fetchers': [
                    {
                        'path': ['key'],
                    },
                ],
            },
        ],
    }

    assert process_raise(
        input_data,
        config,
    ) == [{'name': 'test name'}]


def test_double_repeatable():
    """Test that we can map nested repeatable objects."""
    config = {
        'name': 'root',
        'array': True,
        'iterators': [
            {
                'alias': 'journals',
                'path': ['journals'],
            },
        ],
        'attributes': [
            {
                'name': 'journal_id',
                'data_fetchers': [
                    {
                        'path': ['journals', 'journal', 'id'],
                    },
                ],
            },
        ],
        'objects': [
            {
                'name': 'invoices',
                'array': True,
                'iterators': [
                    {
                        'alias': 'invoices',
                        'path': ['journals', 'journal', 'invoices'],
                    },
                ],
                'attributes': [
                    {
                        'name': 'amount',
                        'data_fetchers': [
                            {
                                'path': ['invoices', 'amount'],
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

    assert process_raise(
        input_data,
        config,
    ) == expected_result


def test_mapping_where_data_is_not_found():
    """Test that when we map and don't find data its okay."""
    config = {
        'name': 'root',
        'array': True,
        'iterators': [
            {
                'alias': 'journals',
                'path': ['journals'],
            },
        ],
        'attributes': [
            {
                'name': 'journal_id',
                'data_fetchers': [
                    {
                        'path': ['journals', 'journal', 'id'],
                    },
                ],
            },
        ],
        'objects': [
            {
                'name': 'invoices',
                'array': True,
                'iterators': [
                    {
                        'alias': 'invoices',
                        'path': ['journals', 'journal', 'invoices'],
                    },
                ],
                'attributes': [
                    {
                        'name': 'amount',
                        'data_fetchers': [
                            {
                                'path': ['invoices', 'amount'],
                            },
                        ],
                    },
                ],
            },
        ],
        'branching_objects': [
            {
                'name': 'extrafield',
                'array': True,
                'branching_attributes': [
                    [
                        {
                            'name': 'datavalue',
                            'data_fetchers': [
                                {
                                    'path': ['extra', 'extra1'],
                                },
                            ],
                        },
                    ],
                ],
            },
        ],
    }
    input_data = {
        'journals': [
            {
                'journal': {
                    'id': 1,
                    'invoices': [{}, {'amount': 1.2}],
                },
            },
            {
                'journal': {
                    'id': 2,
                },
            },
        ],
    }
    expected_result = [
        {
            'journal_id': 1,
            'invoices': [
                {'amount': 1.2},
            ],
        },
        {
            'journal_id': 2,
            'invoices': [],
        },
    ]

    assert process_raise(
        input_data,
        config,
    ) == expected_result


def test_most_features():
    """Test that we can fetch key in dict."""
    config = {
        'name': 'schema',
        'array': False,
        'attributes': [
            {
                'name': 'name',
                'data_fetchers': [
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
                'attributes': [
                    {
                        'name': 'address1',
                        'data_fetchers': [
                            {
                                'path': ['a1'],
                            },
                        ],
                    },
                    {
                        'name': 'address2',
                        'data_fetchers': [
                            {
                                'path': ['a2'],
                            },
                        ],
                    },
                ],
            },
            {
                'name': 'people',
                'array': True,
                'iterators': [
                    {
                        'alias': 'persons',
                        'path': ['persons'],
                    },
                ],
                'attributes': [
                    {
                        'name': 'firstname',
                        'data_fetchers': [
                            {
                                'path': ['persons', 'name'],
                            },
                        ],
                    },
                ],
            },
        ],
        'branching_objects': [
            {
                'name': 'extrafield',
                'array': True,
                'branching_attributes': [
                    [
                        {
                            'name': 'dataname',
                            'default': 'one',
                        },
                        {
                            'name': 'datavalue',
                            'data_fetchers': [
                                {
                                    'path': ['extra', 'extra1'],
                                },
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
                            'data_fetchers': [
                                {
                                    'path': ['extra', 'extra2'],
                                },
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

    assert process_raise(
        input_data,
        config,
    ) == expected_result


def test_regex_feature():  # noqa: WPS210
    """Test Regexp on the example from the docs."""
    with open('tests/json/config_regex.json', 'r') as config_file:
        config = json.load(config_file)

    with open('tests/json/input_regex.json', 'r') as input_file:
        input_data = json.load(input_file)

    with open('tests/json/expected_regex.json', 'r') as expected_file:
        expected_result = json.load(expected_file)

    assert process_raise(
        input_data,
        config,
    ) == expected_result
