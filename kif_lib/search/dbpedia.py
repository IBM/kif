# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import functools
import re

from ..context import Context
from ..model import IRI, Item, T_IRI, Text
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
class DBpediaSearchOptions(HttpxSearchOptions, name='dbpedia'):
    """Empty search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_DBPEDIA_SEARCH_DEBUG',), None)

    DEFAULT_IRI = 'https://lookup.dbpedia.org/api/search'

    _v_iri: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_SEARCH_IRI', 'DBPEDIA_LOOKUP'), DEFAULT_IRI)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_SEARCH_MAX_LIMIT',), None)

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_SEARCH_LANGUAGE',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_SEARCH_LOOKAHEAD',), None)

    DEFAULT_MAX_PAGE_SIZE = 50

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_SEARCH_MAX_PAGE_SIZE',), DEFAULT_MAX_PAGE_SIZE)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_DBPEDIA_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_DBPEDIA_SEARCH_TIMEOUT',), None)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == DBpedia search =======================================================

TOptions: TypeAlias = DBpediaSearchOptions


class DBpediaSearch(
        HttpxSearch[TOptions],
        search_name='dbpedia',
        search_description='DBpedia Lookup API search'
):
    """DBpedia Lookup API search.

    Parameters:
       search_name: Name of the search plugin to instantiate.
       iri: IRI of the target Lookup API.
       kwargs: Other keyword arguments.
    """

    def __init__(
            self,
            search_name: str,
            iri: T_IRI | None = None,
            **kwargs: Any
    ) -> None:
        assert search_name == self.search_name
        super().__init__(search_name, iri=iri, **kwargs)

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cls.get_context(context).options.search.dbpedia

    @override
    def _to_item(self, data: DBpediaSearch.TData) -> Item:
        return Item(data['resource'][0])

    _re_to_item_descritor_label_cleanup: re.Pattern[str] =\
        re.compile(r'</?[a-zA-Z]*>')

    @override
    def to_item_descriptor(
            self,
            data: DBpediaSearch.TData
    ) -> tuple[Item, Item.Descriptor]:
        item = self._to_item(data)
        if 'label' in data:
            label = self._re_to_item_descritor_label_cleanup.sub(
                '', data['label'][0])
            return item, {'labels': {'en': Text(label, 'en')}}
        else:
            return item, {}

    @override
    def _item_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[DBpediaSearch.TData]:
        return self._x_data('item', search, options)

    def _x_data(
            self,
            type: Literal['item', 'lexeme', 'property'],
            search: str,
            options: TOptions
    ) -> Iterator[DBpediaSearch.TData]:
        assert type == 'item', type
        iri, limit = self._check_options(options)
        get_json = functools.partial(self._http_get_json, iri.content)
        data = get_json(self._build_search_params(search, limit))
        if 'docs' in data:
            yield from data['docs']

    def _check_options(
            self,
            options: TOptions
    ) -> tuple[IRI, int]:
        iri = options.iri
        if iri is None:
            assert self.options.DEFAULT_IRI is not None
            iri = IRI(self.options.DEFAULT_IRI)
        limit = options.limit
        if limit is None:
            limit = options.max_limit
        else:
            limit = min(limit, options.max_limit)
        return iri, limit

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
    ) -> AsyncIterator[DBpediaSearch.TData]:
        return self._ax_data('item', search, options)

    async def _ax_data(
            self,
            type: Literal['item', 'lexeme', 'property'],
            search: str,
            options: TOptions
    ) -> AsyncIterator[DBpediaSearch.TData]:
        assert type == 'item', type
        iri, limit = self._check_options(options)
        get_json = functools.partial(self._http_aget_json, iri.content)
        data = await get_json(self._build_search_params(search, limit))
        if 'docs' in data:
            for t in data['docs']:
                yield t
