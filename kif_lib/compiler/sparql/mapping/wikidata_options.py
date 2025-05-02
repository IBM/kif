# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ....context import Section
from ....model import Filter
from ....typing import Any, ClassVar


@dataclasses.dataclass
class WikidataMappingOptions(Section, name='wikidata'):
    """Wikidata SPARQL mapping options."""

    def __init__(self, **kwargs: Any) -> None:
        self._init_blazegraph(kwargs)
        self._init_strict(kwargs)
        self._init_truthy(kwargs)

    # -- blazegraph --

    _v_blazegraph: ClassVar[tuple[str, bool]] =\
        ('KIF_COMPILER_SPARQL_MAPPING_WIKIDATA_BLAZEGRAPH', False)

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
        """Gets the value of the blazegraph flag.

        Returns:
           Blazegraph flag value.
        """
        return self._blazegraph

    def set_blazegraph(self, blazegraph: bool) -> None:
        """Sets the value of the blazegraph flag.

        Parameters:
           blazegraph: Blazegraph flag value.
        """
        self._blazegraph = bool(blazegraph)

    # -- strict --

    _v_strict: ClassVar[tuple[str, bool]] =\
        ('KIF_COMPILER_SPARQL_MAPPING_WIKIDATA_STRICT', False)

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
        """Whether to assume only standard SPARQL compatibility."""
        return not self.strict

    def get_strict(self) -> bool:
        """Gets the value of the strict flag.

        Returns:
           Strict flag value.
        """
        return bool(self._strict)

    def set_strict(self, strict: bool) -> None:
        """Sets the value of the strict flag.

        Parameters:
           strict: Strict flag value or ``None``.
        """
        self._strict = bool(strict)

    # -- truthy --

    _v_truthy: ClassVar[tuple[str, Filter.DatatypeMask]] =\
        ('KIF_COMPILER_SPARQL_MAPPING_WIKIDATA_TRUTHY',
         Filter.DatatypeMask(0))

    _truthy: Filter.DatatypeMask

    def _init_truthy(self, kwargs: dict[str, Any]) -> None:
        self.truthy = kwargs.get(
            '_truthy', self.getenv_int(
                self._v_truthy[0], self._v_truthy[1].value))

    @property
    def truthy(self) -> Filter.DatatypeMask:
        """The truthy mask for filter compilation phase."""
        return self.get_truthy()

    @truthy.setter
    def truthy(self, truthy: Filter.TDatatypeMask) -> None:
        self.set_truthy(truthy)

    def get_truthy(self) -> Filter.DatatypeMask:
        """Gets the truthy mask for the filter compilation phase.

        Returns:
           Datatype mask.
        """
        return self._truthy

    def set_truthy(self, truthy: Filter.TDatatypeMask) -> None:
        """Sets the truthy mask for the filter compilation phase.

        Parameters:
           truthy: Datatype mask.
        """
        self._truthy = Filter.DatatypeMask.check(
            truthy, self.set_truthy, 'truthy', 1)
