# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .abc import Search
from .dbpedia import DBpediaSearch
from .ddgs import DDGS_Search
from .empty import EmptySearch
from .httpx import HttpxSearch
from .wikidata import WikidataSearch
from .wikidata_ddgs import WikidataDDGS_Search

__all__ = (
    'DBpediaSearch',
    'DDGS_Search',
    'EmptySearch',
    'HttpxSearch',
    'Search',
    'WikidataDDGS_Search',
    'WikidataSearch',
)
