# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ... import namespace as NS
from ...context import Section
from ...model import Filter, IRI, Property
from ...typing import Any, cast, ClassVar, Location


@dataclasses.dataclass
class RDF_EncoderOptions(Section, name='rdf'):
    """RDF encoder options."""

    def __init__(self, **kwargs: Any) -> None:
        self._init_define_mask(kwargs)
        self._init_describe_mask(kwargs)
        self._init_schema(kwargs)

    # -- define_mask --

    #: The default value for the define mask option.
    DEFAULT_DEFINE_MASK: ClassVar[Filter.DatatypeMask] = Filter.ENTITY

    _define_mask: Filter.DatatypeMask

    def _init_define_mask(self, kwargs: dict[str, Any]) -> None:
        self.define_mask = kwargs.get(
            '_define_mask', self.DEFAULT_DEFINE_MASK)

    @property
    def define_mask(self) -> Filter.DatatypeMask:
        """The define mask (determine the entities to define)."""
        return self.get_define_mask()

    @define_mask.setter
    def define_mask(self, define_mask: Filter.TDatatypeMask) -> None:
        self.set_define_mask(define_mask)

    def get_define_mask(self) -> Filter.DatatypeMask:
        """Gets the define mask.

        Returns:
           Datatype mask.
        """
        return self._define_mask

    def set_define_mask(
            self,
            define_mask: Filter.TDatatypeMask,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the define mask.

        Parameters:
           define_mask: Datatype mask.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._define_mask = Filter.DatatypeMask.check(
            define_mask, function, name, position)

    # -- describe_mask --

    #: The default value for the describe mask option.
    DEFAULT_DESCRIBE_MASK: ClassVar[Filter.DatatypeMask] =\
        Filter.DatatypeMask(0)

    _describe_mask: Filter.DatatypeMask

    def _init_describe_mask(self, kwargs: dict[str, Any]) -> None:
        self.describe_mask = kwargs.get(
            '_describe_mask', self.DEFAULT_DESCRIBE_MASK)

    @property
    def describe_mask(self) -> Filter.DatatypeMask:
        """The describe mask (determine the entities to describe)."""
        return self.get_describe_mask()

    @describe_mask.setter
    def describe_mask(self, describe_mask: Filter.TDatatypeMask) -> None:
        self.set_describe_mask(describe_mask)

    def get_describe_mask(self) -> Filter.DatatypeMask:
        """Gets the describe mask.

        Returns:
           Datatype mask.
        """
        return self._describe_mask

    def set_describe_mask(
            self,
            describe_mask: Filter.TDatatypeMask,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the describe mask.

        Parameters:
           describe_mask: Datatype mask.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._describe_mask = Filter.DatatypeMask.check(
            describe_mask, function, name, position)

    # -- schema --

    #: The default value for the schema option.
    DEFAULT_SCHEMA: ClassVar[Property.Schema | None] = cast(
        Property.Schema, {
            k: IRI(str(v)) for k, v in NS.Wikidata.prefixes.items()})

    _schema: Property.Schema | None

    def _init_schema(self, kwargs: dict[str, Any]) -> None:
        self._schema = kwargs.get('_schema', self.DEFAULT_SCHEMA)

    @property
    def schema(self) -> Property.Schema | None:
        """The schema to use for properties without schema."""
        return self.get_schema()

    @schema.setter
    def schema(self, schema: Property.TSchema | None) -> None:
        self.set_schema(schema)

    def get_schema(self) -> Property.Schema | None:
        """Gets the schema option.

        Returns:
           Property schema.
        """
        return self._schema

    def set_schema(
            self,
            schema: Property.TSchema | None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the schema option.

        Parameters:
           schema: Property schema.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._schema = Property._check_optional_schema(
            schema, None, function, name, position)


@dataclasses.dataclass
class RDF_Options(Section, name='rdf'):
    """RDF codec options."""

    encoder: RDF_EncoderOptions = dataclasses.field(
        default_factory=RDF_EncoderOptions)
