# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..engine import _EngineOptions
from ..typing import Any, override
from .abc import _SearchOptions
from .dbpedia import DBpediaSearchOptions
from .dbpedia_ddgs import DBpediaDDGS_SearchOptions
from .ddgs import DDGS_SearchOptions
from .empty import EmptySearchOptions
from .httpx import HttpxSearchOptions
from .pubchem import PubChemSearchOptions
from .wikidata import WikidataSearchOptions
from .wikidata_ddgs import WikidataDDGS_SearchOptions


@dataclasses.dataclass
class SearchOptions(_SearchOptions, name='search'):
    """Search options."""

    dbpedia: DBpediaSearchOptions = dataclasses.field(
        default_factory=DBpediaSearchOptions)

    dbpedia_ddgs: DBpediaDDGS_SearchOptions = dataclasses.field(
        default_factory=DBpediaDDGS_SearchOptions)

    ddgs: DDGS_SearchOptions = dataclasses.field(
        default_factory=DDGS_SearchOptions)

    empty: EmptySearchOptions = dataclasses.field(
        default_factory=EmptySearchOptions)

    httpx: HttpxSearchOptions = dataclasses.field(
        default_factory=HttpxSearchOptions)

    pubchem: PubChemSearchOptions = dataclasses.field(
        default_factory=PubChemSearchOptions)

    wikidata: WikidataSearchOptions = dataclasses.field(
        default_factory=WikidataSearchOptions)

    wikidata_ddgs: WikidataDDGS_SearchOptions = dataclasses.field(
        default_factory=WikidataDDGS_SearchOptions)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.dbpedia = DBpediaSearchOptions()
        self.dbpedia_ddgs = DBpediaDDGS_SearchOptions()
        self.ddgs = DDGS_SearchOptions()
        self.empty = EmptySearchOptions()
        self.httpx = HttpxSearchOptions()
        self.pubchem = PubChemSearchOptions()
        self.wikidata = WikidataSearchOptions()
        self.wikidata_ddgs = WikidataDDGS_SearchOptions()

    @override
    def _get_parent_callback(self) -> _EngineOptions:
        return self.get_context().options.engine
