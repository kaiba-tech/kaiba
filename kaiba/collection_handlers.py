from typing import Any, Dict, List, Union

from returns.result import Failure, ResultE, Success, safe

from kaiba.models.base import AnyType
from kaiba.models.iterator import Iterator


@safe
def set_value_in_dict(
    new_value: AnyType,
    collection: Dict[str, Any],
    path: List[str],
) -> None:
    """Set value in a dict(pass by ref) by path."""
    if not path:
        raise ValueError('path list empty')

    for key in path[:-1]:
        # this will return a Failure[KeyError] if not found
        collection = collection[key]

    collection[path[-1]] = new_value


@safe
def fetch_data_by_keys(
    collection: Union[Dict[str, AnyType], List[AnyType]],
    path: List[Union[str, int]],
) -> AnyType:
    """Find data in collection by following a list of path."""
    if not path:
        raise ValueError('path list empty')

    for key in path:
        # this will return a Failure[KeyError] if not found
        collection = collection[key]  # type: ignore

    return collection


@safe
def fetch_list_by_keys(
    collection: Dict[str, AnyType],
    path: List[Union[str, int]],
) -> list:
    """Find data that *must* be a list else it fails.

    Example
        >>> fetch_list_by_keys(
        ...     {'object': {'some_list': ['1']}}, ['object', 'some_list'],
        ... ).unwrap()
        ['1']
    """
    if not path:
        raise ValueError('path list empty')

    for key in path:
        # this will return a Failure[KeyError] if not found
        collection = collection[key]  # type: ignore

    if isinstance(collection, list):  # type: ignore
        return collection  # type: ignore

    raise ValueError('Non list data found: ', str(collection))


def iterable_data_handler(
    raw_data: dict,
    iterators: List[Iterator],
) -> ResultE[list]:
    """Iterate and create all combinations from list of iterators."""
    if not iterators:
        return Failure(ValueError('No iterators'))

    iterable, rest = iterators[0], iterators[1:]

    if not rest:
        return create_iterable(raw_data, iterable)

    my_list: list = []

    for iterable_list in create_iterable(raw_data, iterable).unwrap():

        iterable_data_handler(iterable_list, rest).map(
            my_list.extend,
        )

    return Success(my_list)


def create_iterable(
    input_data: dict,
    iterable: Iterator,
) -> ResultE[list]:
    """Return set of set of data per entry in list at iterable[path]."""
    return fetch_list_by_keys(
        input_data,
        iterable.path,
    ).map(
        lambda collections: [
            {
                **input_data,
                **{iterable.alias: collection},
            }
            for collection in collections
        ],
    ).lash(
        lambda _: Success([input_data]),
    )
