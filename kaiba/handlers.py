from typing import Any, Dict, List, Optional, Union

from returns.result import Failure, ResultE, Success

from kaiba.collection_handlers import fetch_data_by_keys, unsafe_fetch_data_by_keys
from kaiba.functions import (
    apply_casting,
    apply_if_statements,
    apply_regex,
    apply_separator,
    apply_slicing,
    unsafe_apply_casting,
    unsafe_apply_if_statements,
    unsafe_apply_regex,
    unsafe_apply_separator,
)
from kaiba.models.attribute import Attribute
from kaiba.models.base import AnyType
from kaiba.models.data_fetcher import DataFetcher


def handle_data_fetcher(
    collection: Union[Dict[str, Any], List[Any]],
    cfg: DataFetcher,
) -> ResultE[AnyType]:
    """Find a data at path or produce a value.

    return value can be:
    - value found at path
    - value found but sliced
    - value found applied to regular expression
    - conditional value depending on if statements
    - default value if all the above still produces `None`

    Flow description:

    find data from path or None ->
    apply regular expression ->
    apply slicing ->
    apply if statements ->
    return default value if Failure else mapped value
    """

    produced_value = None

    produced_value = unsafe_fetch_data_by_keys(
        collection, path=cfg.path,
    )

    if produced_value and cfg.regex:
        produced_value = unsafe_apply_regex(produced_value, regex=cfg.regex)

    if produced_value and cfg.slicing:
        produced_value = apply_slicing(produced_value, cfg.slicing)

    produced_value = unsafe_apply_if_statements(
        produced_value,
        cfg.if_statements,
    )

    if produced_value is None:

        if cfg.default is not None:
            return Success(cfg.default)

        return Failure(ValueError('Failed to produce a value'))

    return Success(produced_value)


def unsafe_handle_data_fetcher(
    collection: Union[Dict[str, Any], List[Any]],
    cfg: DataFetcher,
) -> Optional[AnyType]:
    """Find a data at path or produce a value.

    return value can be:
    - value found at path
    - value found but sliced
    - value found applied to regular expression
    - conditional value depending on if statements
    - default value if all the above still produces `None`

    Flow description:

    find data from path or None ->
    apply regular expression ->
    apply slicing ->
    apply if statements ->
    return default value if Failure else mapped value
    """

    produced_value = None

    produced_value = unsafe_fetch_data_by_keys(
        collection, path=cfg.path,
    )

    if produced_value and cfg.regex:
        produced_value = unsafe_apply_regex(produced_value, regex=cfg.regex)

    if produced_value and cfg.slicing:
        produced_value = apply_slicing(produced_value, cfg.slicing)

    produced_value = unsafe_apply_if_statements(
        produced_value,
        cfg.if_statements,
    )

    if produced_value is None:
        return cfg.default

    return produced_value


def handle_attribute(
    collection: Union[Dict[str, Any], List[Any]],
    cfg: Attribute,
) -> ResultE[AnyType]:
    """Handle one attribute with data fetchers, ifs, casting and default value.

    flow description:

    Fetch once for all data in Attribute.data_fetchers ->
    Apply separator to values if there are more than 1
    Failure -> fix to Success(None)
    Apply if statements
    Success -> Cast Value
    Failure -> apply default value

    Return Result
    """

    fetched_values = [
        fetched
        for fetched in [  # noqa: WPS361
            unsafe_handle_data_fetcher(collection, data_fetcher)
            for data_fetcher in cfg.data_fetchers
        ]
        if fetched is not None
    ]

    attribute = None

    if fetched_values:
        attribute = unsafe_apply_separator(
            fetched_values,
            separator=cfg.separator,
        )

    attribute = unsafe_apply_if_statements(attribute, cfg.if_statements)

    if attribute and cfg.casting:
        attribute = unsafe_apply_casting(attribute, cfg.casting)


    if attribute is None:

        if cfg.default is not None:
            return Success(cfg.default)

        return Failure(ValueError('Failed to produce a value'))

    return Success(attribute)
