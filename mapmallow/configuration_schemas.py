# -*- coding: utf-8 -*-

"""Validation functions for mapping configuration data."""
from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates_schema,
)
from typing_extensions import final

from mapmallow.constants import (  # noqa: WPS235
    CONTAINS,
    DATE,
    DECIMAL,
    DEFAULT,
    DMY_DATE_FORMAT,
    INTEGER,
    INTEGER_CONTAINING_DECIMALS,
    IS,
    ITERATE,
    MAPPINGS,
    MDY_DATE_FORMAT,
    NOT,
    ORIGINAL_FORMAT,
    PATH,
    PATH_TO_ITERABLE,
    TO,
    YMD_DATE_FORMAT,
)


@final
class ConfigIfStatement(Schema):
    """Schema class for If Statements objects in configuration file."""

    condition = fields.String(
        required=True,
        validate=validate.OneOf([IS, NOT, CONTAINS]),
    )
    target = fields.Raw(required=True, allow_none=True)
    then = fields.Raw(required=True, allow_none=True)
    otherwise = fields.Raw()


@final
class ConfigCasting(Schema):
    """Schema class for Casting objects in configuration file."""

    # Check decimals and dates in YMD, DMY and MDY formats
    regexp = '({0}|{1}|{2}|{3}|{4})'.format(
        DECIMAL,
        INTEGER_CONTAINING_DECIMALS,
        DMY_DATE_FORMAT,
        MDY_DATE_FORMAT,
        YMD_DATE_FORMAT,
    )

    to = fields.String(
        required=True,
        validate=validate.OneOf([INTEGER, DECIMAL, DATE]),
    )
    original_format = fields.String(
        validate=validate.Regexp(regexp),
        missing=None,
    )

    @validates_schema
    def _original_format_required_when_to_is_date(
        self, data, **kwargs,
    ) -> None:

        to_date = data[TO] == DATE
        missing_original_format = not data[ORIGINAL_FORMAT]
        if to_date and missing_original_format:
            raise ValidationError(
                'original_format requried when to equals date',
            )


@final
class ConfigMapping(Schema):
    """Schema class for mapping objects in configuration file."""

    path = fields.List(fields.Raw)
    if_statements = fields.List(
        fields.Nested(ConfigIfStatement),
        missing=[],
    )
    default = fields.Raw(missing=None)

    @validates_schema
    def _path_or_default_required(self, data, **kwargs) -> None:
        not_path = PATH not in data or not data[PATH]
        not_default = DEFAULT not in data

        if not_path and not_default:
            raise ValidationError(
                'path or default required',
            )


@final
class ConfigAttribute(Schema):
    """Schema class for attribute objects in configuration file."""

    name = fields.String(required=True)
    mappings = fields.List(
        fields.Nested(ConfigMapping),
        missing=[],
    )
    separator = fields.String(missing='')
    if_statements = fields.List(
        fields.Nested(ConfigIfStatement),
        missing=[],
    )
    casting = fields.Nested(ConfigCasting, missing={})
    default = fields.Raw(missing=None)

    # if no mappings, then a default needs to exist
    @validates_schema
    def _mappings_or_default_required(self, data, **kwargs) -> None:
        default = DEFAULT not in data or data[DEFAULT] is None

        mappings = MAPPINGS not in data or not data[MAPPINGS]

        if default and mappings:
            raise ValidationError(
                'mappings required if not default is provided',
            )


@final
class ConfigBranchingObject(Schema):
    """Schema for branching objects in configuration file."""

    name = fields.String(required=True)
    array = fields.Boolean(required=True)
    iterate = fields.Boolean(missing=False)
    path_to_iterable = fields.List(fields.String)

    branching_attributes = fields.List(
        fields.List(fields.Nested(ConfigAttribute)),
        required=True,
    )

    @validates_schema
    def _path_to_iterable_required_when_iterate_true(
        self, data, **kwargs,
    ) -> None:
        if ITERATE in data and data[ITERATE] is True:
            if PATH_TO_ITERABLE not in data:
                raise ValidationError(
                    'path_to_iterable required if iterate is True',
                )


@final
class ConfigObject(Schema):
    """Base class and entry point of configuration files."""

    name = fields.String(required=True)
    array = fields.Boolean(required=True)
    iterate = fields.Boolean(missing=False)
    path_to_iterable = fields.List(fields.String)

    objects = fields.List(
        fields.Nested(lambda: ConfigObject()),  # noqa: WPS506
        missing=[],
    )
    branching_objects = fields.List(
        fields.Nested(ConfigBranchingObject),
        missing=[],
    )
    attributes = fields.List(
        fields.Nested(ConfigAttribute),
        missing=[],
    )

    @validates_schema
    def _path_to_iterable_required_when_iterate_true(
        self, data, **kwargs,
    ) -> None:
        if ITERATE in data and data[ITERATE] is True:
            if PATH_TO_ITERABLE not in data:
                raise ValidationError(
                    'path_to_iterable required if iterate is True',
                )

    @validates_schema
    def _one_of_children_required(self, data, **kwargs) -> None:
        objects = 'objects' not in data or not data['objects']
        attributes = 'attributes' not in data or not data['attributes']
        b_objects = 'branching_objects' not in data
        b_objects = b_objects or not data['branching_objects']

        if objects and attributes and b_objects:
            raise ValidationError(
                'Objects, attributes or branching_objects is required',
            )
