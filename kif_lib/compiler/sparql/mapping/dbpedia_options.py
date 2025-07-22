# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ....context import Section
from ....typing import Any, ClassVar, Location


@dataclasses.dataclass
class DBpediaMappingOptions(Section, name='dbpedia'):
    """PubChem SPARQL mapping options."""

    def __init__(self, **kwargs: Any) -> None:
        self._init_wikidata_properties(kwargs)

    # -- wikidata_properties --

    #: The default value for the Wikidata properties option.
    DEFAULT_WIKIDATA_PROPERTIES: ClassVar[bool] = True

    _v_wikidata_properties: ClassVar[tuple[str, bool]] =\
        ('KIF_COMPILER_SPARQL_MAPPING_DBPEDIA_WIKIDATA_PROPERTIES',
         DEFAULT_WIKIDATA_PROPERTIES)

    _wikidata_properties: bool

    def _init_wikidata_properties(self, kwargs: dict[str, Any]) -> None:
        self.wikidata_properties = kwargs.get(
            '_wikidata_properties', self.getenv_bool(
                *self._v_wikidata_properties))

    @property
    def wikidata_properties(self) -> bool:
        """Whether to match (equivalent) Wikidata properties."""
        return self.get_wikidata_properties()

    @wikidata_properties.setter
    def wikidata_properties(self, wikidata_properties: bool) -> None:
        self.set_wikidata_properties(wikidata_properties)

    def get_wikidata_properties(self) -> bool:
        """Gets the Wikidata properties flag.

        Returns:
           Wikidata properties flag.
        """
        return self._wikidata_properties

    def set_wikidata_properties(
            self,
            wikidata_properties: bool,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the Wikidata properties flag.

        Parameters:
           wikidata_properties: Wikidata properties flag.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._wikidata_properties = bool(wikidata_properties)
