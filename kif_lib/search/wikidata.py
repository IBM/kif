# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..model import T_IRI
from ..typing import Any, Literal, TypedDict
from .httpx import HttpxSearch


class WikidataSearch(
        HttpxSearch,
        search_name='wikidata',
        search_description='Wikidata MediaWiki API search'
):
    """Wikidata MediaWiki API search.

    Parameters:
       search_name: Name of the search plugin to instantiate.
       iri: IRI of the target MediaWiki API.
       kwargs: Other keyword arguments.
    """

    #: Parameters of the wbsearchentities action.
    SearchEntitiesParams = TypedDict('SearchEntitiesParams', {
        'action': Literal['wbsearchentities'],
        'search': str,
        'language': str,
        'type': str,
        'limit': int,
        'continue': int,
        'format': str,
    })

    def __init__(
            self,
            search_name: str,
            iri: T_IRI | None = None,
            **kwargs: Any
    ) -> None:
        assert search_name == self.search_name
        super().__init__(search_name, iri=iri, **kwargs)
