# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import collections
import dataclasses
import re

from ..context import Context
from ..model import IRI, Item, Lexeme, Property, Text
from ..namespace import Wikidata
from ..typing import (
    Any,
    ClassVar,
    Final,
    Iterable,
    Iterator,
    Literal,
    override,
    TypeAlias,
)
from .wikidata_wapi import WikidataWAPI_Search, WikidataWAPI_SearchOptions


@dataclasses.dataclass
class WikidataREST_SearchOptions(
        WikidataWAPI_SearchOptions,
        name='wikidata_rest'
):
    """Wikidata REST search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_WIKIDATA_REST_SEARCH_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_REST_SEARCH_MAX_LIMIT',), None)

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_REST_SEARCH_LANGUAGE',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_REST_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_REST_SEARCH_LOOKAHEAD',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_REST_SEARCH_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_REST_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_WIKIDATA_REST_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_WIKIDATA_REST_SEARCH_TIMEOUT',), None)

    # -- httpx --

    DEFAULT_IRI = 'https://www.wikidata.org/w/rest.php'

    _v_iri: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_REST_SEARCH_IRI', 'WIKIDATA_REST'), DEFAULT_IRI)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == Wikidata REST search ==================================================

TOptions: TypeAlias = WikidataREST_SearchOptions


class WikidataREST_Search(
        WikidataWAPI_Search[TOptions],
        search_name='wikidata-rest',
        search_description='Wikidata REST search'
):
    """Wikidata REST search.

    Parameters:
       search_name: Name of the search plugin to instantiate.
       kwargs: Other keyword arguments.
    """

    def __init__(self, search_name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(search_name, *args, **kwargs)

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cls.get_context(context).options.search.wikidata_rest

    _re_item: Final[re.Pattern[str]] = re.compile(r'^Q\d+$')
    _re_lexeme: Final[re.Pattern[str]] = re.compile(r'^L\d+$')
    _re_property: Final[re.Pattern[str]] = re.compile(r'^P\d+$')

    @override
    def _to_item(self, data: WikidataWAPI_Search.TData) -> Item:
        id = data['id']
        if self._re_item.match(id):
            return Item(Wikidata.WD[id])
        else:
            raise ValueError

    @override
    def _to_lexeme(self, data: WikidataWAPI_Search.TData) -> Lexeme:
        id = data['id']
        if self._re_lexeme.match(data['id']):
            return Lexeme(Wikidata.WD[id])
        else:
            raise ValueError

    @override
    def _to_property(self, data: WikidataWAPI_Search.TData) -> Property:
        id = data['id']
        if self._re_property.match(id):
            return Property(Wikidata.WD[id])
        else:
            raise ValueError

    @override
    def _to_x_descriptor(
            self,
            data: WikidataWAPI_Search.TData,
            empty: dict[str, Any] = {}
    ) -> dict[str, Any]:
        try:
            res: dict[str, Any] = collections.defaultdict(dict)
            if 'description' in data:
                desc = data['description']
                res['descriptions'][desc['language']] =\
                    Text(desc['value'], desc['language'])
            if 'display-label' in data:
                label = data['display-label']
                res['labels'][label['language']] =\
                    Text(label['value'], label['language'])
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

    _check_options_type_plural: Final[dict[
        Literal['item', 'lexeme', 'property'], str]] = {
            'item': 'items',
            'lexeme': 'lexemes',
            'property': 'properties'}

    def _check_options(
            self,
            type: Literal['item', 'lexeme', 'property'],
            options: TOptions
    ) -> tuple[IRI, str, int, int, float | None]:
        iri, *args = super()._check_options(type, options)
        plural = self._check_options_type_plural[type]
        iri = IRI(f"{iri.content.rstrip('/')}/wikibase/v0/search/{plural}")
        return iri, *args       # type: ignore

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
        yield ('q', search)
        if language is not None:
            yield ('language', language)
        if limit is not None:
            yield ('limit', limit)
        if offset is not None:
            yield ('offset', offset)

    def _x_data_parse(
            self,
            response: dict[str, Any]
    ) -> list[WikidataWAPI_Search.TData]:
        return response.get('results', [])
