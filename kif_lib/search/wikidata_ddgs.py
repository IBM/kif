# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..context import Context
from ..typing import (
    Any,
    AsyncIterator,
    ClassVar,
    Iterable,
    Iterator,
    override,
    TypeAlias,
)
from .ddgs import DDGS_Search, DDGS_SearchOptions


@dataclasses.dataclass
class WikidataDDGS_SearchOptions(DDGS_SearchOptions, name='wikidata_ddgs'):
    """Wikidata DDGS search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_MAX_LIMIT',), None)

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_LANGUAGE',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_LOOKAHEAD',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_TIMEOUT',), None)

    # -- ddgs --

    _v_backend: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_BACKEND'), None)

    DEFAULT_ITEM_MATCH =\
        r'^http[s]?://www\.wikidata\.org/(entity/Q|wiki/Q)(\d+)$'

    _v_item_match: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_ITEM_MATCH'), DEFAULT_ITEM_MATCH)

    DEFAULT_ITEM_SUB = r'http://www.wikidata.org/entity/Q\2'

    _v_item_sub: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_ITEM_SUB'), DEFAULT_ITEM_SUB)

    DEFAULT_LEXEME_MATCH =\
        r'^http[s]?://www\.wikidata\.org/(entity/L|wiki/Lexeme:L)(\d+)$'

    _v_lexeme_match: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_LEXEME_MATCH'), DEFAULT_LEXEME_MATCH)

    DEFAULT_LEXEME_SUB = r'http://www.wikidata.org/entity/L\2'

    _v_lexeme_sub: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_LEXEME_SUB'), DEFAULT_LEXEME_SUB)

    DEFAULT_PROPERTY_MATCH =\
        r'^http[s]?://www\.wikidata\.org/(entity/P|wiki/Property:P)(\d+)$'

    _v_property_match: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_PROPERTY_MATCH'), DEFAULT_PROPERTY_MATCH)

    DEFAULT_PROPERTY_SUB = r'http://www.wikidata.org/entity/P\2'

    _v_property_sub: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_PROPERTY_SUB'), DEFAULT_PROPERTY_SUB)

    DEFAULT_SITE = 'http://www.wikidata.org/'

    _v_site: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_WIKIDATA_DDGS_SEARCH_SITE'), DEFAULT_SITE)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == Wikidata DDGS search ==================================================

TOptions: TypeAlias = WikidataDDGS_SearchOptions


class WikidataDDGS_Search(
        DDGS_Search[TOptions],
        search_name='wikidata-ddgs',
        search_description='Wikidata DDGS search'
):
    """Wikidata DDGS search.

    Parameters:
       search_name: Name of the search plugin to instantiate.
       kwargs: Other keyword arguments.
    """

    def __init__(self, search_name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(search_name, *args, **kwargs)

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cls.get_context(context).options.search.wikidata_ddgs

    @override
    def _lexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[WikidataDDGS_Search.TData]:
        options.in_url = 'lexeme'
        return super()._lexeme_data(search, options)

    @override
    def _property_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[WikidataDDGS_Search.TData]:
        options.in_url = 'property'
        return super()._property_data(search, options)

    @override
    def _alexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[WikidataDDGS_Search.TData]:
        options.in_url = 'lexeme'
        return super()._alexeme_data(search, options)

    @override
    def _aproperty_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[WikidataDDGS_Search.TData]:
        options.in_url = 'property'
        return super()._aproperty_data(search, options)
