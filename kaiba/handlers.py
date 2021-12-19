from typing import Any, Dict, List, Union

from returns.curry import partial
from returns.pipeline import flow, is_successful
from returns.pointfree import bind, fix, map_, rescue
from returns.result import Failure, ResultE, Success, safe

from kaiba.collection_handlers import fetch_data_by_keys, unsafe_fetch_data_by_keys
from kaiba.functions import (
    apply_casting,
    apply_default,
    apply_if_statements,
    apply_regex,
    apply_separator,
    apply_slicing,
    unsafe_apply_default,
    unsafe_apply_if_statements,
    unsafe_apply_regex,
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

    produced_value = apply_slicing(produced_value, cfg.slicing)

    produced_value = unsafe_apply_if_statements(
        produced_value,
        cfg.if_statements,
    )

    produced_value = unsafe_apply_default(
        produced_value,
        cfg.default,
    )

    if produced_value:
        return Success(produced_value)

    return Failure('Failed to produce a value')


    # return produced_value


    return flow(
        collection,
        partial(fetch_data_by_keys, path=cfg.path),
        fix(lambda _: None),  # type: ignore
        bind(
            partial(
                apply_regex, regex=cfg.regex,
            ),
        ),
        fix(lambda _: None),  # type: ignore
        map_(partial(
            apply_slicing, slicing=cfg.slicing,
        )),
        bind(partial(
            apply_if_statements, statements=cfg.if_statements,
        )),
        rescue(  # type: ignore
            lambda _: apply_default(cfg.default),
        ),
    )


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
        fetched.unwrap()
        for fetched in  # noqa: WPS361
        [
            handle_data_fetcher(collection, data_fetcher)
            for data_fetcher in cfg.data_fetchers
        ]
        if is_successful(fetched)
    ]

    # partially declare if statement and casting functions
    ifs = partial(apply_if_statements, statements=cfg.if_statements)

    cast = safe(lambda the_value: the_value)
    if cfg.casting:
        cast = partial(apply_casting, casting=cfg.casting)

    return flow(
        apply_separator(fetched_values, separator=cfg.separator),
        fix(lambda _: None),  # type: ignore
        bind(ifs),
        bind(cast),
        rescue(
            lambda _: apply_default(default=cfg.default),
        ),
    )
