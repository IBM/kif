# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ....context import Section
from ....model import Filter
from ....typing import Any, ClassVar, Location


@dataclasses.dataclass
class WikidataMappingOptions(Section, name='wikidata'):
    """Wikidata SPARQL mapping options."""

    def __init__(self, **kwargs: Any) -> None:
        self._init_blazegraph(kwargs)
        self._init_strict(kwargs)
        self._init_truthy(kwargs)

    # -- blazegraph --

    #: The default value for the blazegraph flag option.
    DEFAULT_BLAZEGRAPH: ClassVar[bool] = False

    _v_blazegraph: ClassVar[tuple[str, bool]] =\
        ('KIF_COMPILER_SPARQL_MAPPING_WIKIDATA_BLAZEGRAPH',
         DEFAULT_BLAZEGRAPH)

    _blazegraph: bool

    def _init_blazegraph(self, kwargs: dict[str, Any]) -> None:
        self.blazegraph = kwargs.get(
            '_blazegraph', self.getenv_bool(*self._v_blazegraph))

    @property
    def blazegraph(self) -> bool:
        """Whether to target Blazegraph (use named subqueries)."""
        return self.get_blazegraph()

    @blazegraph.setter
    def blazegraph(self, blazegraph: bool) -> None:
        self.set_blazegraph(blazegraph)

    def get_blazegraph(self) -> bool:
        """Gets the blazegraph flag.

        Returns:
           Blazegraph flag.
        """
        return self._blazegraph

    def set_blazegraph(
            self,
            blazegraph: bool,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the blazegraph flag.

        Parameters:
           blazegraph: Blazegraph flag.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._blazegraph = bool(blazegraph)

    # -- strict --

    #: The default value of the strict option.
    DEFAULT_STRICT: ClassVar[bool] = False

    _v_strict: ClassVar[tuple[str, bool]] =\
        ('KIF_COMPILER_SPARQL_MAPPING_WIKIDATA_STRICT', DEFAULT_STRICT)

    _strict: bool

    def _init_strict(self, kwargs: dict[str, Any]) -> None:
        self.strict = kwargs.get(
            '_strict', self.getenv_bool(*self._v_strict))

    @property
    def strict(self) -> bool:
        """Whether to assume full Wikidata SPARQL compatibility."""
        return self.get_strict()

    @strict.setter
    def strict(self, strict: bool) -> None:
        self.set_strict(strict)

    @property
    def relax(self) -> bool:
        """Whether to assume standard SPARQL compatibility."""
        return not self.strict

    def get_strict(self) -> bool:
        """Gets the strict flag.

        Returns:
           Strict flag.
        """
        return bool(self._strict)

    def set_strict(
            self,
            strict: bool,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the strict flag.

        Parameters:
           strict: Strict flag.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._strict = bool(strict)

    # -- truthy --

    #: The default value of the truthy option.
    DEFAULT_TRUTHY: ClassVar[Filter.DatatypeMask] = Filter.DatatypeMask(0)

    _truthy: Filter.DatatypeMask

    def _init_truthy(self, kwargs: dict[str, Any]) -> None:
        self.truthy = kwargs.get('_truthy', self.DEFAULT_TRUTHY)

    @property
    def truthy(self) -> Filter.DatatypeMask:
        """The truthy mask (used in filter compilation phase)."""
        return self.get_truthy()

    @truthy.setter
    def truthy(self, truthy: Filter.TDatatypeMask) -> None:
        self.set_truthy(truthy)

    def get_truthy(self) -> Filter.DatatypeMask:
        """Gets the truthy mask phase.

        Returns:
           Datatype mask.
        """
        return self._truthy

    def set_truthy(
            self,
            truthy: Filter.TDatatypeMask,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the truthy mask.

        Parameters:
           truthy: Datatype mask.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._truthy = Filter.DatatypeMask.check(
            truthy, function, name, position)
