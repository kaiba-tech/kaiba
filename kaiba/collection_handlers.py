from typing import Any, Dict, List, Union

from returns.result import Failure, ResultE, Success, safe

from kaiba.pydantic_schema import Iterable
from kaiba.valuetypes import MapValue


@safe
def set_value_in_dict(
    new_value: MapValue,
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
    collection: Union[Dict[str, Any], List[Any]],
    path: List[Union[str, int]],
) -> MapValue:
    """Find data in collection by following a list of path."""
    if not path:
        raise ValueError('path list empty')

    for key in path:
        # this will return a Failure[KeyError] if not found
        collection = collection[key]  # type: ignore

    return collection  # type: ignore


@safe
def fetch_list_by_keys(
    collection: Dict[str, Any],
    path: List[str],
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
        collection = collection[key]

    if isinstance(collection, list):  # type: ignore
        return collection  # type: ignore

    raise ValueError('Non list data found: ', str(collection))


def iterable_data_handler(
    raw_data,
    iterables: List[Iterable],
) -> ResultE[list]:
    """Iterate and create all combinations from list of iterables."""
    if not iterables:
        return Failure(ValueError('No iterables'))

    iterable, rest = iterables[0], iterables[1:]

    if not rest:
        return create_iterable(raw_data, iterable)

    my_list: list = []

    for iterable_list in create_iterable(raw_data, iterable).unwrap():

        iterable_data_handler(iterable_list, rest).map(
            my_list.extend,
        )

    return Success(my_list)


def create_iterable(
    input_data,
    iterable: Iterable,
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
    ).fix(
        lambda _: [input_data],
    )
