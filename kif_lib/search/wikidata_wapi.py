# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import collections
import dataclasses
import re

from .. import functools, itertools
from ..context import Context
from ..model import IRI, Item, Lexeme, Property, Text
from ..namespace import Wikidata
from ..typing import (
    Any,
    AsyncIterator,
    cast,
    ClassVar,
    Final,
    Iterable,
    Iterator,
    Literal,
    Mapping,
    override,
    TypeVar,
)
from .httpx import HttpxSearch, HttpxSearchOptions


@dataclasses.dataclass
class WikidataWAPI_SearchOptions(HttpxSearchOptions, name='wikidata_wapi'):
    """Wikidata Wikibase API search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_WIKIDATA_WAPI_SEARCH_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_WAPI_SEARCH_MAX_LIMIT',), None)

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_WAPI_SEARCH_LANGUAGE',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_WAPI_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_WAPI_SEARCH_LOOKAHEAD',), None)

    DEFAULT_MAX_PAGE_SIZE = 50

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_WAPI_SEARCH_MAX_PAGE_SIZE',), DEFAULT_MAX_PAGE_SIZE)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_WAPI_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_WIKIDATA_WAPI_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_WIKIDATA_WAPI_SEARCH_TIMEOUT',), None)

    # -- httpx --

    DEFAULT_IRI = 'https://www.wikidata.org/w/api.php'

    _v_iri: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_WAPI_SEARCH_IRI', 'WIKIDATA_WAPI'), DEFAULT_IRI)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == Wikidata WAPI search ==================================================

TOptions = TypeVar(
    'TOptions',
    bound=WikidataWAPI_SearchOptions,
    default=WikidataWAPI_SearchOptions)


class WikidataWAPI_Search(
        HttpxSearch[TOptions],
        search_name='wikidata-wapi',
        search_aliases=['wikidata'],
        search_description='Wikidata Wikibase API search'
):
    """Wikidata Wikibase API search with "wbsearchentities" action.

    Parameters:
       search_name: Name of the search plugin to instantiate.
       kwargs: Other keyword arguments.
    """

    def __init__(self, search_name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(search_name, *args, **kwargs)

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cast(TOptions, cls.get_context(
            context).options.search.wikidata_wapi)

    @override
    def _to_item(self, data: WikidataWAPI_Search.TData) -> Item:
        return Item(data['concepturi'])

    @override
    def to_item_descriptor(
            self,
            data: WikidataWAPI_Search.TData
    ) -> tuple[Item, Item.Descriptor]:
        return (self._to_item(data), cast(
            Item.Descriptor, self._to_x_descriptor(data)))

    @override
    def _to_lexeme(self, data: WikidataWAPI_Search.TData) -> Lexeme:
        return Lexeme(data['concepturi'])

    @override
    def to_lexeme_descriptor(
            self,
            data: WikidataWAPI_Search.TData
    ) -> tuple[Lexeme, Lexeme.Descriptor]:
        lexeme = self._to_lexeme(data)
        try:
            m = data['match']
            if m['type'] == 'label':
                lang, text = m['language'], m['text']
                return lexeme, {'lemma': Text(text, lang)}
        except Exception:
            pass
        return lexeme, {}

    @override
    def _to_property(self, data: WikidataWAPI_Search.TData) -> Property:
        return Property(data['concepturi'], data['datatype'])

    @override
    def to_property_descriptor(
            self,
            data: WikidataWAPI_Search.TData
    ) -> tuple[Property, Property.Descriptor]:
        prop = self._to_property(data)
        desc = self._to_x_descriptor(data)
        desc['range'] = prop.range
        return prop, cast(Property.Descriptor, desc)

    def _to_x_descriptor(
            self,
            data: WikidataWAPI_Search.TData,
            empty: dict[str, Any] = {}
    ) -> dict[str, Any]:
        try:
            res: dict[str, Any] = collections.defaultdict(dict)
            if 'label' in data:
                res['labels']['en'] = Text(data['label'], 'en')
            if 'description' in data:
                res['descriptions']['en'] = Text(data['description'], 'en')
            if 'match' in data:
                m = data['match']
                lang, text = m['language'], m['text']
                if m['type'] == 'label':
                    res['labels'][lang] = Text(text, lang)
                elif m['type'] == 'alias':
                    res['aliases'][lang] = {Text(text, lang)}
            return dict(res)
        except KeyError:
            return empty

    @override
    def _item_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[WikidataWAPI_Search.TData]:
        return self._x_data('item', search, options)

    @override
    def _lexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[WikidataWAPI_Search.TData]:
        return self._x_data('lexeme', search, options)

    @override
    def _property_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[WikidataWAPI_Search.TData]:
        return self._x_data('property', search, options)

    def _x_data(
            self,
            type: Literal['item', 'lexeme', 'property'],
            search: str,
            options: TOptions
    ) -> Iterator[WikidataWAPI_Search.TData]:
        iri, language, limit, page_size = self._check_options(type, options)
        get_json = functools.partial(self._http_get_json, iri.content)
        stream = self._build_search_entities_params_stream(
            search, type, 'json', language, page_size)
        count = 0
        while count < limit:
            res = self._x_data_parse(get_json(next(stream)))
            if not res:
                break
            yield from res
            n = len(res)
            if n < page_size:
                break
            count += n

    def _check_options(
            self,
            type: Literal['item', 'lexeme', 'property'],
            options: TOptions
    ) -> tuple[IRI, str, int, int]:
        iri = options.iri
        if iri is None:
            assert self.options.DEFAULT_IRI is not None
            iri = IRI(self.options.DEFAULT_IRI)
        language = options.language
        assert language is not None
        limit = options.limit
        if limit is None:
            limit = options.max_limit
        else:
            limit = min(limit, options.max_limit)
        page_size = min(options.page_size, limit, options.max_page_size)
        return iri, language, limit, page_size

    def _build_search_entities_params_stream(
            self,
            search: str,
            type: Literal['item', 'lexeme', 'property'],
            format: str,
            language: str,
            limit: int
    ) -> Iterator[Mapping[str, int | str]]:
        offset = 0
        while True:
            yield dict(self._build_search_entities_params_tail(
                search, type, format, language, limit, offset))
            offset += limit

    def _build_search_entities_params_tail(
            self,
            search: str,
            type: Literal['item', 'lexeme', 'property'],
            format: str | None = None,
            language: str | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> Iterator[tuple[str, int | str]]:
        yield ('action', 'wbsearchentities')
        yield ('search', search)
        yield ('type', type)
        if format is not None:
            yield ('format', format)
        if language is not None:
            yield ('language', language)
        if limit is not None:
            yield ('limit', limit)
        if offset is not None:
            yield ('continue', offset)

    def _x_data_parse(
            self,
            response: dict[str, Any]
    ) -> list[WikidataWAPI_Search.TData]:
        return response.get('search', [])

    @override
    def _aitem_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[WikidataWAPI_Search.TData]:
        return self._ax_data('item', search, options)

    @override
    def _alexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[WikidataWAPI_Search.TData]:
        return self._ax_data('lexeme', search, options)

    @override
    def _aproperty_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[WikidataWAPI_Search.TData]:
        return self._ax_data('property', search, options)

    async def _ax_data(
            self,
            type: Literal['item', 'lexeme', 'property'],
            search: str,
            options: TOptions
    ) -> AsyncIterator[WikidataWAPI_Search.TData]:
        iri, language, limit, page_size = self._check_options(type, options)
        get_json = functools.partial(self._http_aget_json, iri.content)
        stream = self._build_search_entities_params_stream(
            search, type, 'json', language, page_size)
        count = 0
        for batch in itertools.batched(stream, options.lookahead):
            tasks = (asyncio.ensure_future(get_json(p)) for p in batch)
            for res in map(self._x_data_parse, await asyncio.gather(*tasks)):
                if not res:
                    return      # nothing to do
                for t in res:
                    yield t
                n = len(res)
                if n < page_size:
                    return
                count += n
                if count == limit:
                    return


# == Wikidata WAPI query search ============================================

class WikidataWAPI_QuerySearch(
        WikidataWAPI_Search,
        search_name='wikidata-wapi-query',
        search_description='Wikidata Wikibase API search ("query" action)'
):
    """Alias for :class:`WikidataWAPI_Search` using "query" action."""

    def __init__(self, search_name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(search_name, *args, **kwargs)

    _re_item: Final[re.Pattern[str]] = re.compile(r'^Q\d+$')

    @override
    def _to_item(self, data: WikidataWAPI_Search.TData) -> Item:
        if self._re_item.match(data['title']):
            return Item(Wikidata.WD[data['title']])
        else:
            raise ValueError

    @override
    def to_item_descriptor(
            self,
            data: WikidataWAPI_Search.TData
    ) -> tuple[Item, Item.Descriptor]:
        if 'snippet' in data:
            return (self._to_item(data), {
                'descriptions': {'en': Text(data['snippet'], 'en')}})
        else:
            return (self._to_item(data), {})

    @override
    def to_lexeme(self, data: WikidataWAPI_Search.TData) -> Lexeme:
        raise NotImplementedError

    @override
    def to_lexeme_descriptor(
            self,
            data: WikidataWAPI_Search.TData
    ) -> tuple[Lexeme, Lexeme.Descriptor]:
        raise NotImplementedError

    @override
    def to_property(self, data: WikidataWAPI_Search.TData) -> Property:
        raise NotImplementedError

    @override
    def to_property_descriptor(
            self,
            data: WikidataWAPI_Search.TData
    ) -> tuple[Property, Property.Descriptor]:
        raise NotImplementedError

    @override
    def _build_search_entities_params_tail(
            self,
            search: str,
            type: Literal['item', 'lexeme', 'property'],
            format: str | None = None,
            language: str | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> Iterator[tuple[str, int | str]]:
        yield ('action', 'query')
        yield ('list', 'search')
        yield ('srsearch', search)
        if format is not None:
            yield ('format', format)
        if limit is not None:
            yield ('srlimit', limit)
        if offset is not None:
            yield ('sroffset', offset)

    @override
    def _lexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[WikidataWAPI_Search.TData]:
        return iter(())

    @override
    def _property_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[WikidataWAPI_Search.TData]:
        return iter(())

    @override
    def _x_data_parse(
            self,
            response: dict[str, Any]
    ) -> list[WikidataWAPI_Search.TData]:
        return response['query']['search']

    @override
    def _alexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[WikidataWAPI_Search.TData]:
        return self._asearch_empty_iterator()

    @override
    def _aproperty_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[WikidataWAPI_Search.TData]:
        return self._asearch_empty_iterator()
