# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .abc import Search
from .dbpedia_ddgs import DBpediaDDGS_Search
from .dbpedia_lookup import DBpediaLookupSearch
from .ddgs import DDGS_Search
from .empty import EmptySearch
from .httpx import HttpxSearch
from .pubchem_ddgs import PubChemDDGS_Search
from .pubchem_pug import PubChemPUG_Search
from .wikidata_ddgs import WikidataDDGS_Search
from .wikidata_wapi import WikidataWAPI_QuerySearch, WikidataWAPI_Search

__all__ = (
    'DBpediaDDGS_Search',
    'DBpediaLookupSearch',
    'DDGS_Search',
    'EmptySearch',
    'HttpxSearch',
    'PubChemDDGS_Search',
    'PubChemPUG_Search',
    'Search',
    'WikidataDDGS_Search',
    'WikidataWAPI_QuerySearch',
    'WikidataWAPI_Search',
)
