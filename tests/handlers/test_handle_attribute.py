import decimal

from kaiba.handlers import handle_attribute
from kaiba.models.attribute import Attribute


def test_get_key_in_dict():
    """Test that we can fetch key in dict."""
    input_data = {'key': 'val1'}
    config = Attribute(**{
        'name': 'attrib',
        'data_fetchers': [
            {'path': ['key']},
        ],
    })

    assert handle_attribute(
        input_data,
        config,
    ).unwrap() == 'val1'


def test_casting_to_decimal():
    """Test that we can cast a string value to decimal."""
    input_data = {'key': '1,123,123.12'}
    config = Attribute(**{
        'name': 'attrib',
        'data_fetchers': [
            {'path': ['key']},
        ],
        'casting': {'to': 'decimal'},
    })

    assert handle_attribute(
        input_data,
        config,
    ).unwrap() == decimal.Decimal('1123123.12')


def test_regex_is_applied_to_attribute():
    """Test that we can expression by pattern."""
    input_data: dict = {'game': '1. e4 e5 ... 14. Rxe8+ Rxe8'}
    config = Attribute(**{
        'name': 'moves',
        'data_fetchers': [
            {
                'path': ['game'],
                'regex': {
                    'expression': '(Rxe8)',
                    'group': 1,
                },
            },
        ],
    })
    assert handle_attribute(
        input_data,
        config,
    ).unwrap() == 'Rxe8'


def test_regex_is_not_applied_to_attribute():
    """Test that we _do_ lose data when expression by pattern fails."""
    input_data: dict = {'game': '1. d4 d5'}
    config = Attribute(**{
        'name': 'moves',
        'data_fetchers': [
            {
                'path': ['game'],
                'regex': {
                    'expression': '(d6)',
                    'group': 0,
                },
            },
        ],
    })
    regex = handle_attribute(input_data, config)
    assert isinstance(regex.failure(), ValueError) is True
    assert regex.failure().args == ('Failed to produce a value',)


def test_all():
    """Test a full attribute schema."""
    input_data = {'key': 'val1', 'key2': 'val2'}
    config = Attribute(**{
        'name': 'attrib',
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
    })

    assert handle_attribute(
        input_data,
        config,
    ).unwrap() == 'default2'
