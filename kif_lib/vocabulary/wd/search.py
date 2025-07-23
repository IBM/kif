# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
import json
import logging

import httpx

from ...context import Context
from ...model import (
    Entity,
    IRI,
    Item,
    KIF_Object,
    Lexeme,
    Property,
    TTextLanguage,
)
from ...typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Final,
    Iterator,
    Literal,
    Location,
    Mapping,
    override,
    TypedDict,
)
from ..search import Search

_logger: Final[logging.Logger] = logging.getLogger(__name__)


class WikidataSearch(Search):

    #: Default IRI of Wikidata MediaWiki Action API.
    _default_wapi_iri: ClassVar[IRI] =\
        IRI('https://www.wikidata.org/w/api.php')

    #: Maximum limit supported by the API.
    _maximum_wapi_limit: ClassVar[int] = 50

    #: Parameters of the API wbsearchentities action.
    SearchParams = TypedDict('SearchParams', {
        'action': Literal['wbsearchentities'],
        'search': str,
        'language': str,
        'type': str,
        'limit': int,
        'continue': int,
        'format': str,
    })

    __slots__ = (
        '_iri'
    )

    #: The URI of Wikidata MediaWiki API.
    _iri: IRI

    def __init__(
            self,
            iri: IRI | None = None,
            headers: Search.HTTP_Headers | None = None,
            **kwargs: Any
    ) -> None:
        super().__init__(headers=headers, **kwargs)
        self._iri = cast(IRI, IRI.check_optional(
            iri, self._default_wapi_iri, type(self), 'iri'))

    @override
    def _search(
            self,
            search: str,
            type: Literal['item', 'lexeme', 'property'],
            language: TTextLanguage | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            context: Context | None = None
    ) -> Iterator[tuple[Entity, dict[str, Any]]]:
        limit, page_size, mk_params = self._prepare_search(
            search, type, language, limit, page_size, context, self._search)
        offset = 0
        while limit:
            res = self._do_search(mk_params(offset))
            try:
                for t in res['search']:
                    yield self._parse_search_results_entry(type, t)
                    limit -= 1
                    if limit == 0:
                        break
                if len(res['search']) < page_size:
                    break
                offset += page_size
            except KeyError as err:
                _logger.error('bad wbsearchentities response: %s', res)
                raise err

    def _do_search(
            self,
            params: WikidataSearch.SearchParams
    ) -> dict[str, Any]:
        res = self._http_get(
            self._iri.content,
            params=cast(Mapping[str, int | str], params),
            timeout=httpx.Timeout(self._timeout))
        try:
            return res.json()
        except json.JSONDecodeError:
            raise self.Error(res.text)

    async def _do_asearch(
            self,
            params: WikidataSearch.SearchParams
    ) -> dict[str, Any]:
        res = await self._http_aget(
            self._iri.content,
            params=cast(Mapping[str, int | str], params),
            timeout=httpx.Timeout(self._timeout))
        try:
            return res.json()
        except json.JSONDecodeError:
            raise self.Error(res.text)

    def _prepare_search(
            self,
            search: str,
            type: Literal['item', 'lexeme', 'property'],
            language: TTextLanguage | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            context: Context | None = None,
            location: Location | None = None,
    ) -> tuple[int, int, Callable[[int], WikidataSearch.SearchParams]]:
        language = self._check_optional_language(
            language, self._search)
        if language is not None:
            lang = language.content
        else:
            lang = self.get_context(context).options.language
        limit = self._check_optional_limit(limit, self._search)
        if limit is None:
            limit = self.get_context(context).options.store.max_limit
        else:
            limit = max(limit, 0)
        page_size = self._check_optional_page_size(page_size, self._search)
        if page_size is None:
            page_size = self._maximum_wapi_limit
        else:
            page_size = max(min(page_size, self._maximum_wapi_limit), 1)
        return limit, page_size, functools.partial(
            self._build_search_params,
            search, type, lang, page_size, format='json')

    def _build_search_params(
            self,
            search: str,
            type: Literal['item', 'lexeme', 'property'],
            language: str,
            limit: int,
            offset: int,
            format: str
    ) -> WikidataSearch.SearchParams:
        return {
            'action': 'wbsearchentities',
            'search': search,
            'type': type,
            'language': language,
            'limit': limit,
            'continue': offset,
            'format': format,
        }

    def _parse_search_results_entry(
            self,
            type: Literal['item', 'lexeme', 'property'],
            t: dict[str, Any]
    ) -> tuple[Entity, dict[str, Any]]:
        if type == 'item':
            return Item(t['concepturi']), t
        elif type == 'lexeme':
            return Lexeme(t['concepturi']), t
        elif type == 'property':
            return Property(t['concepturi'], t['datatype']), t
        raise KIF_Object._should_not_get_here()
