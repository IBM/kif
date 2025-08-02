# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..engine import _EngineOptions
from ..typing import Any, override
from .abc import _SearchOptions
from .dbpedia_ddgs import DBpediaDDGS_SearchOptions
from .dbpedia_lookup import DBpediaLookupSearchOptions
from .ddgs import DDGS_SearchOptions
from .empty import EmptySearchOptions
from .httpx import HttpxSearchOptions
from .pubchem_pug import PubChemPUG_SearchOptions
from .wikidata_ddgs import WikidataDDGS_SearchOptions
from .wikidata_rest import WikidataREST_SearchOptions
from .wikidata_wapi import WikidataWAPI_SearchOptions


@dataclasses.dataclass
class SearchOptions(_SearchOptions, name='search'):
    """Search options."""

    dbpedia_ddgs: DBpediaDDGS_SearchOptions = dataclasses.field(
        default_factory=DBpediaDDGS_SearchOptions)

    dbpedia_lookup: DBpediaLookupSearchOptions = dataclasses.field(
        default_factory=DBpediaLookupSearchOptions)

    ddgs: DDGS_SearchOptions = dataclasses.field(
        default_factory=DDGS_SearchOptions)

    empty: EmptySearchOptions = dataclasses.field(
        default_factory=EmptySearchOptions)

    httpx: HttpxSearchOptions = dataclasses.field(
        default_factory=HttpxSearchOptions)

    pubchem_pug: PubChemPUG_SearchOptions = dataclasses.field(
        default_factory=PubChemPUG_SearchOptions)

    wikidata_ddgs: WikidataDDGS_SearchOptions = dataclasses.field(
        default_factory=WikidataDDGS_SearchOptions)

    wikidata_rest: WikidataREST_SearchOptions = dataclasses.field(
        default_factory=WikidataREST_SearchOptions)

    wikidata_wapi: WikidataWAPI_SearchOptions = dataclasses.field(
        default_factory=WikidataWAPI_SearchOptions)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.dbpedia_ddgs = DBpediaDDGS_SearchOptions()
        self.dbpedia_lookup = DBpediaLookupSearchOptions()
        self.ddgs = DDGS_SearchOptions()
        self.empty = EmptySearchOptions()
        self.httpx = HttpxSearchOptions()
        self.pubchem_pug = PubChemPUG_SearchOptions()
        self.wikidata_ddgs = WikidataDDGS_SearchOptions()
        self.wikidata_rest = WikidataREST_SearchOptions()
        self.wikidata_wapi = WikidataWAPI_SearchOptions()

    @override
    def _get_parent_callback(self) -> _EngineOptions:
        return self.get_context().options.engine
