from kaiba.collection_handlers import iterable_data_handler
from kaiba.pydantic_schema import Iterable


def test_iterable_data_handler():
    """Test that we can iterate multiple levels in one go."""
    input_data = {
        'data': [
            {'nested': [
                {'another': [
                    {'a': 'a'},
                    {'a': 'b'},
                ]},
            ]},
            {'nested': [
                {'another': [
                    {'a': 'c'},
                    {'a': 'd'},
                ]},
            ]},
        ],
    }

    paths_to_iterables = [
        Iterable(**{
            'alias': 'data',
            'path': ['data'],
        }),
        Iterable(**{
            'alias': 'nested',
            'path': ['data', 'nested'],
        }),
        Iterable(**{
            'alias': 'doesnotexist',
            'path': ['does', 'not', 'exist'],
        }),
        Iterable(**{
            'alias': 'another',
            'path': ['nested', 'another'],
        }),
    ]

    iterables = iterable_data_handler(input_data, paths_to_iterables).unwrap()
    assert len(iterables) == 4
    assert iterables[3]['another']['a'] == 'd'


def test_iterable_no_paths_returns_failure():
    """Test that when there are no paths we get a Failure."""
    iterables = iterable_data_handler({}, [])
    assert 'No iterables' in str(iterables.failure())
