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
        self._init_define(kwargs)
        self._init_schema(kwargs)

    # -- define --

    #: The default value for the define option.
    DEFAULT_DEFINE: ClassVar[Filter.DatatypeMask] = Filter.ENTITY

    _define: Filter.DatatypeMask

    def _init_define(self, kwargs: dict[str, Any]) -> None:
        self.define = kwargs.get('_define', self.DEFAULT_DEFINE)

    @property
    def define(self) -> Filter.DatatypeMask:
        """The define mask (determine the entities to define)."""
        return self.get_define()

    @define.setter
    def define(self, define: Filter.TDatatypeMask) -> None:
        self.set_define(define)

    def get_define(self) -> Filter.DatatypeMask:
        """Gets the define mask.

        Returns:
           Datatype mask.
        """
        return self._define

    def set_define(
            self,
            define: Filter.TDatatypeMask,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the define mask.

        Parameters:
           define: Datatype mask.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._define = Filter.DatatypeMask.check(
            define, function, name, position)

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
