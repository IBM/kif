# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import collections
import dataclasses
import functools

from ..context import Context
from ..model import IRI, Item, Lexeme, Property, T_IRI, Text
from ..typing import (
    Any,
    cast,
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
class WikidataSearchOptions(HttpxSearchOptions, name='wikidata'):
    """Empty search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_WIKIDATA_SEARCH_DEBUG',), None)

    DEFAULT_IRI = 'https://www.wikidata.org/w/api.php'

    _v_iri: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_SEARCH_IRI', 'WIKIDATA_WAPI'), DEFAULT_IRI)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_SEARCH_MAX_LIMIT',), None)

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_SEARCH_LANGUAGE',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_SEARCH_LOOKAHEAD',), None)

    DEFAULT_MAX_PAGE_SIZE = 50

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_SEARCH_MAX_PAGE_SIZE',), DEFAULT_MAX_PAGE_SIZE)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_WIKIDATA_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_WIKIDATA_SEARCH_TIMEOUT',), None)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == Wikidata search =======================================================

TOptions: TypeAlias = WikidataSearchOptions


class WikidataSearch(
        HttpxSearch[TOptions],
        search_name='wikidata',
        search_description='Wikidata MediaWiki API search'
):
    """Wikidata MediaWiki API search.

    Parameters:
       search_name: Name of the search plugin to instantiate.
       iri: IRI of the target MediaWiki API.
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
        return cls.get_context(context).options.search.wikidata

    @override
    def _to_item(self, data: WikidataSearch.TData) -> Item:
        return Item(data['concepturi'])

    @override
    def to_item_descriptor(
            self,
            data: WikidataSearch.TData
    ) -> tuple[Item, Item.Descriptor]:
        return (self._to_item(data), cast(
            Item.Descriptor, self._to_x_descriptor(data)))

    @override
    def _to_lexeme(self, data: WikidataSearch.TData) -> Lexeme:
        return Lexeme(data['concepturi'])

    @override
    def to_lexeme_descriptor(
            self,
            data: WikidataSearch.TData
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
    def _to_property(self, data: WikidataSearch.TData) -> Property:
        return Property(data['concepturi'], data['datatype'])

    @override
    def to_property_descriptor(
            self,
            data: WikidataSearch.TData
    ) -> tuple[Property, Property.Descriptor]:
        prop = self._to_property(data)
        desc = self._to_x_descriptor(data)
        desc['range'] = prop.range
        return prop, cast(Property.Descriptor, desc)

    def _to_x_descriptor(
            self,
            data: WikidataSearch.TData,
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
    ) -> Iterator[WikidataSearch.TData]:
        return self._x_data('item', search, options)

    @override
    def _lexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[WikidataSearch.TData]:
        return self._x_data('lexeme', search, options)

    @override
    def _property_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[WikidataSearch.TData]:
        return self._x_data('property', search, options)

    def _x_data(
            self,
            type: Literal['item', 'lexeme', 'property'],
            search: str,
            options: TOptions
    ) -> Iterator[WikidataSearch.TData]:
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
        assert limit is not None
        page_size = min(options.page_size, options.max_page_size)
        get_json = functools.partial(self._http_get_json, iri.content)
        mk_params = functools.partial(
            self._build_search_entities_params,
            search, type, 'json', options.language, page_size)
        count, offset = 0, 0
        while count < limit:
            res = get_json(mk_params(offset))
            if 'search' not in res:
                break           # nothing to do
            yield from res['search']
            n = len(res['search'])
            if n < page_size:
                break
            offset += page_size
            count += n

    def _build_search_entities_params(
            self,
            search: str,
            type: Literal['item', 'lexeme', 'property'],
            format: str | None = None,
            language: str | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> Mapping[str, int | str]:
        return dict(self._build_search_entities_params_tail(
            search, type, format, language, limit, offset))

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
