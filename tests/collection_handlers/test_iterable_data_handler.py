import pytest

from kaiba.collection_handlers import iterable_data_handler
from kaiba.models.iterator import Iterator


def test_iterable_handler_one_iterator():
    """Test that we can iterate multiple levels in one go."""
    input_data = {
        'data': [
            {'nested': [
                {'another': [
                    {'a': 'a'},
                    {'a': 'b'},
                ]},
                {'another': [
                    {'a': 'c'},
                    {'a': 'd'},
                ]},
            ]},
        ],
    }

    iterators = [
        Iterator(**{
            'alias': 'nested_item',
            'path': ['data', 0, 'nested'],
        }),
    ]

    iteration_list = iterable_data_handler(
        input_data,
        iterators,
    )
    assert len(iteration_list) == 2
    print(iteration_list)
    assert iteration_list[1]['nested_item']['another'][1]['a'] == 'd'


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
        Iterator(**{
            'alias': 'data',
            'path': ['data'],
        }),
        Iterator(**{
            'alias': 'nested',
            'path': ['data', 'nested'],
        }),
        Iterator(**{
            'alias': 'doesnotexist',
            'path': ['does', 'not', 'exist'],
        }),
        Iterator(**{
            'alias': 'another',
            'path': ['nested', 'another'],
        }),
    ]

    iterables = iterable_data_handler(input_data, paths_to_iterables)
    assert len(iterables) == 4
    assert iterables[3]['another']['a'] == 'd'


def test_iterable_no_paths_returns_failure():
    """Test that when there are no paths we get a Failure."""
    with pytest.raises(ValueError) as ve:
        iterable_data_handler({}, [])

    assert 'No iterators' in str(ve.value)
