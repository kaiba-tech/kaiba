# -*- coding: utf-8 -*-

"""Code for handling marshmallow schemas load, dump and validation errors.

# TODO: monkey patch returns._Failure.map_failure to alt so that we can use
both returns 0.9.0 and newer versions.

"""
from typing import Any, Callable, Set, cast

from attr import dataclass
from marshmallow import Schema, ValidationError, fields, missing
from returns.pipeline import flow, is_successful
from returns.pointfree import alt, bind, rescue
from returns.result import Result, safe
from typing_extensions import final

from mapmallow.collection_handlers import (
    FetchDataByKeys,
    FetchListByKeys,
    SetValueInDict,
)
from mapmallow.error_handlers import error_dict_as_list_of_tuples
from mapmallow.valuetypes import MapResult


@final
@dataclass(frozen=True, slots=True)
class ApplySchema(object):
    """Load data to model and dump processed data."""

    schema: Schema
    rescue_functions: Set[Callable] = set()

    _error_converter: Callable = error_dict_as_list_of_tuples
    _fetch_value: Callable = FetchDataByKeys()
    _fetch_collection: Callable = FetchListByKeys()
    _set_value: Callable = SetValueInDict()

    def __call__(self, dictionary: dict) -> Result[dict, Exception]:
        """Validate and produce output."""
        return flow(
            dictionary,
            self._load,
            rescue(self._rescue),
            alt(lambda validation_error: validation_error.messages),  # type: ignore  # noqa: E501
            bind(self._dump),
        )

    @safe
    def _load(self, dictionary: dict) -> dict:
        return self.schema.load(dictionary)

    @safe
    def _dump(self, dictionary: dict) -> dict:
        return self.schema.dump(dictionary)

    def _rescue(  # noqa: WPS210, WPS231 allow these variables and complexity.
        self, validation_error: Exception,
    ) -> Result[dict, Any]:
        """Apply functions in _rescue_functions to all errors and load again.

        get errors as list of path to each error and loop it
        since errors come in lists, get the collection and loop per error_msg
        send original_value and error_msg to all fixer functions
        set new value to the correct key in the input data
        return self._load that loads the data into the schema again

        we skip if we can't find the list of errors for a path
        we skip if we can't find the original value
        """
        validation_error = cast(ValidationError, validation_error)
        paths = self._error_converter(validation_error.messages)
        if not is_successful(paths):
            raise RuntimeError(
                'Unable to create list of errors',
                validation_error.messages,
            )

        for path in paths.unwrap():
            error_messages = self._fetch_collection(
                validation_error.messages, path,
            ).value_or([])

            for error_msg in error_messages:

                original_value = self._fetch_value(validation_error.data, path)
                if not is_successful(original_value):
                    continue

                new_value = original_value.unwrap()

                for func in self.rescue_functions:
                    new_value = func(new_value, error_msg).value_or(new_value)

                self._set_value(
                    new_value,
                    validation_error.data,
                    path,
                )
        return self._load(validation_error.data)

    @safe
    def _ignore(self, validation_error: ValidationError) -> MapResult:
        raise validation_error


@final
@dataclass(slots=True, frozen=True)
class MakeConfigurationSkeleton(object):
    """Take a Marshmallow schema and return a mapping configuration json."""

    def __call__(self, schema) -> Result[dict, Exception]:
        """Create a configuration skeleton with given schema recursively."""
        return self._handle_object(schema)

    @safe
    def _handle_object(
        self,
        schema: Schema,
        name: str = 'root',
        array: bool = False,
    ) -> dict:
        """Make json representation of schema with types etc."""
        schema_fields = schema.fields

        skeleton: dict = {
            'name': name,
            'array': array,
            'iterate': False,
            'path_to_iterable': [],
            'attributes': [],
            'objects': [],
            'branching_objects': [],
        }

        for key, field in schema_fields.items():

            # handle objects
            # handle attribute
            if isinstance(field, fields.List):
                # this might actually be a list of attributes??? idk
                self._handle_object(
                    field.inner.schema,
                    key,
                    True,  # noqa: WPS319, WPS425
                ).map(
                    skeleton['objects'].append,
                )
            elif isinstance(field, fields.Nested):
                self._handle_object(field.schema, key).map(
                    skeleton['objects'].append,
                )
            else:
                self._handle_attribute(field, key).map(
                    skeleton['attributes'].append,
                )

        return skeleton

    @safe
    def _handle_attribute(
        self,
        field: fields.Field,
        name: str,
    ) -> dict:
        """Return an attribute."""
        mis = None
        if not isinstance(field.missing, type(missing)):
            mis = field.missing
        return {
            'meta': {
                'type': type(field).__name__,
                'required': field.required,
                'missing': mis,
                'allow_none': field.allow_none,
            },
            'name': name,
            'mappings': [],
            'if_statements': [],
            'separator': '',
            'default': None,
        }
