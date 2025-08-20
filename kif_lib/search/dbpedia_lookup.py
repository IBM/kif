# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import re

from ..context import Context
from ..model import IRI, Item, Text
from ..typing import (
    Any,
    AsyncIterator,
    ClassVar,
    Iterable,
    Iterator,
    Literal,
    Mapping,
    override,
    TypeAlias,
)
from .httpx import HttpxSearch, HttpxSearchOptions


@dataclasses.dataclass
class DBpediaLookupSearchOptions(HttpxSearchOptions, name='dbpedia_lookup'):
    """DBpedia search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_DBPEDIA_LOOKUP_SEARCH_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_LOOKUP_SEARCH_MAX_LIMIT',), None)

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_LOOKUP_SEARCH_LANGUAGE',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_LOOKUP_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_LOOKUP_SEARCH_LOOKAHEAD',), None)

    DEFAULT_MAX_PAGE_SIZE = 50

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_LOOKUP_SEARCH_MAX_PAGE_SIZE',), DEFAULT_MAX_PAGE_SIZE)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_LOOKUP_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_DBPEDIA_LOOKUP_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_DBPEDIA_LOOKUP_SEARCH_TIMEOUT',), None)

    # -- httpx --

    DEFAULT_IRI = 'https://lookup.dbpedia.org/api/search'

    _v_iri: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_LOOKUP_SEARCH_IRI', 'DBPEDIA_LOOKUP'), DEFAULT_IRI)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == DBpedia search =======================================================

TOptions: TypeAlias = DBpediaLookupSearchOptions


class DBpediaLookupSearch(
        HttpxSearch[TOptions],
        search_name='dbpedia-lookup',
        search_aliases=['dbpedia'],
        search_description='DBpedia Lookup API search'
):
    """DBpedia Lookup API search.

    Parameters:
       search_name: Name of the search plugin to instantiate.
       kwargs: Other keyword arguments.
    """

    def __init__(self, search_name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(search_name, *args, **kwargs)

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cls.get_context(context).options.search.dbpedia_lookup

    @override
    def _to_item(self, data: DBpediaLookupSearch.TData) -> Item:
        return Item(data['resource'][0])

    _re_to_item_descritor_cleanup: re.Pattern[str] =\
        re.compile(r'</?[a-zA-Z]*>')

    @override
    def to_item_descriptor(
            self,
            data: DBpediaLookupSearch.TData
    ) -> tuple[Item, Item.Descriptor]:
        item = self._to_item(data)
        desc: Item.Descriptor = {}
        if 'label' in data:
            label = self._re_to_item_descritor_cleanup.sub(
                '', data['label'][0])
            desc['labels'] = {'en': Text(label, 'en')}
        if 'comment' in data:
            description = self._re_to_item_descritor_cleanup.sub(
                '', data['comment'][0])
            desc['descriptions'] = {'en': Text(description, 'en')}
        return item, desc

    @override
    def _item_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[DBpediaLookupSearch.TData]:
        return self._x_data('item', search, options)

    def _x_data(
            self,
            type: Literal['item', 'lexeme', 'property'],
            search: str,
            options: TOptions
    ) -> Iterator[DBpediaLookupSearch.TData]:
        assert type == 'item', type
        iri, limit, timeout = self._check_options(options)
        data = self._http_get_json(
            iri.content, self._build_search_params(search, limit), timeout)
        if 'docs' in data:
            yield from data['docs']

    def _check_options(
            self,
            options: TOptions
    ) -> tuple[IRI, int, float | None]:
        iri = options.iri
        if iri is None:
            assert self.options.DEFAULT_IRI is not None
            iri = IRI(self.options.DEFAULT_IRI)
        limit = options.limit
        if limit is None:
            limit = options.max_limit
        else:
            limit = min(limit, options.max_limit)
        timeout = options.timeout
        return iri, limit, timeout

    def _build_search_params(
            self,
            search: str,
            limit: int
    ) -> Mapping[str, int | str]:
        return dict(format='JSON', maxResults=limit, query=search)

    @override
    def _aitem_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[DBpediaLookupSearch.TData]:
        return self._ax_data('item', search, options)

    async def _ax_data(
            self,
            type: Literal['item', 'lexeme', 'property'],
            search: str,
            options: TOptions
    ) -> AsyncIterator[DBpediaLookupSearch.TData]:
        assert type == 'item', type
        iri, limit, timeout = self._check_options(options)
        data = await self._http_aget_json(
            iri.content, self._build_search_params(search, limit), timeout)
        if 'docs' in data:
            for t in data['docs']:
                yield t
