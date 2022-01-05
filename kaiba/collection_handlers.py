from typing import Any, Dict, List, Optional, Union

from kaiba.models.base import AnyType
from kaiba.models.iterator import Iterator


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


def fetch_data_by_keys(
    collection: Union[Dict[str, AnyType], List[AnyType]],
    path: List[Union[str, int]],
) -> Optional[AnyType]:
    """Find data in collection by following a list of path."""
    if not path:
        return None

    try:
        for key in path:
            # this will return a Failure[KeyError] if not found
            collection = collection[key]  # type: ignore
    except KeyError:
        return None

    return collection


def fetch_list_by_keys(
    collection: Dict[str, AnyType],
    path: List[Union[str, int]],
) -> list:
    """Find data that *must* be a list else it fails.

    Example
        >>> fetch_list_by_keys(
        ...     {'object': {'some_list': ['1']}}, ['object', 'some_list'],
        ... )
        ['1']
    """
    if not path:
        raise ValueError('path list empty')

    for key in path:
        # this will raise a KeyError if not found
        collection = collection[key]  # type: ignore

    if isinstance(collection, list):  # type: ignore
        return collection  # type: ignore

    raise ValueError('Non list data found: ', str(collection))


def iterable_data_handler(
    raw_data: dict,
    iterators: List[Iterator],
) -> list:
    """Iterate and create all combinations from list of iterators."""
    if not iterators:
        raise ValueError('No iterators')

    iterable, rest = iterators[0], iterators[1:]

    if not rest:
        print('mjau')
        return create_iterable(raw_data, iterable)

    my_list: list = []

    for iterable_list in create_iterable(raw_data, iterable):

        try:
            my_list.extend(iterable_data_handler(iterable_list, rest))
        except Exception:  # noqa: S110
            pass  # noqa: WPS420

    return my_list


def create_iterable(
    input_data: dict,
    iterator: Iterator,
) -> list:
    """Return set of set of data per entry in list at iterator[path]."""
    iterator_items = []

    try:
        iterator_items = fetch_list_by_keys(
            input_data,
            iterator.path,
        )
    except ValueError:
        return [input_data]
    except KeyError:
        return [input_data]

    print('got here')
    return [
        {
            **input_data,
            **{iterator.alias: collection},
        }
        for collection in iterator_items
    ]
