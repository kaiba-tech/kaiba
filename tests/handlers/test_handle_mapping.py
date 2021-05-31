from returns.pipeline import is_successful
from returns.result import Success

from kaiba.handlers import handle_mapping
from kaiba.pydantic_schema import Mapping


def test_get_string_value_from_key():
    """Test that we can find value."""
    input_data = {'key': 'val1'}
    config = Mapping(**{'path': ['key']})

    assert handle_mapping(
        input_data,
        config,
    ) == Success('val1')


def test_get_array_value_from_key():
    """Test that we can find an array."""
    input_data = {'key': ['array']}
    config = Mapping(**{'path': ['key']})

    assert handle_mapping(
        input_data,
        config,
    ) == Success(['array'])


def test_get_object_value_from_key():
    """Test that we can find an object."""
    input_data = {'key': {'obj': 'val1'}}
    config = Mapping(**{'path': ['key']})

    assert handle_mapping(
        input_data,
        config,
    ) == Success({'obj': 'val1'})


def test_default_value_is_used():
    """Test that we get a default value when no path and no ifs."""
    input_data = {'key': 'val'}
    config = Mapping(**{'default': 'default'})

    assert handle_mapping(
        input_data, config,
    ).unwrap() == 'default'


def test_regexp_is_applied():
    """Test that we can search by pattern."""
    input_data: dict = {'game': '8. d4 Re8 ... 14. Rxe8+ Rxe8 15. h3'}  # noqa: E501
    config = Mapping(**{
        'path': ['game'],
        'regexp': {
            'search': '(Rxe8.*)',
        },
    })
    assert handle_mapping(
        input_data,
        config,
    ).unwrap() == 'Rxe8+ Rxe8 15. h3'


def test_regexp_is_applied_on_group_as_list():
    """Test that we can search by pattern when it is a list."""
    input_data: dict = {'game': '1. e4 e5 6. Qe2+ Qe7 7. Qxe7+ Kxe7 8. d4 Re8'}
    config = Mapping(**{
        'path': ['game'],
        'regexp': {
            'search': r'(e\d)+',
            'group': [0, 1, 6],
        },
    })
    assert handle_mapping(
        input_data,
        config,
    ).unwrap() == ['e4', 'e5', 'e8']


def test_slicing_is_applied():
    """Test that applying slicing works."""
    input_data = {'key': 'value'}
    config = Mapping(**{
        'path': ['key'],
        'slicing': {
            'from': 2,
            'to': 3,
        },
    })
    assert handle_mapping(
        input_data, config,
    ).unwrap() == 'l'


def test_if_statements_are_applied():
    """Test that applying if statements works."""
    input_data = {'key': 'val'}
    config = Mapping(**{
        'if_statements': [{
            'condition': 'is',
            'target': None,
            'then': 'otherval',
        }],
        'default': 'bob',
    })
    assert handle_mapping(
        input_data, config,
    ).unwrap() == 'otherval'


def test_default_value_not_none():
    """Test that providing bad data returns Failure instance."""
    failure = handle_mapping(
        {'fail': 'failure'},
        Mapping(**{'path': [], 'default': None}),
    )
    assert not is_successful(failure)
    assert 'Default value should not be `None`' in str(failure.failure())
