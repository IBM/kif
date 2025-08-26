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
class DBpediaDDGS_SearchOptions(DDGS_SearchOptions, name='dbpedia_ddgs'):
    """DBpedia DDGS search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_MAX_LIMIT',), None)

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_LANGUAGE',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_LOOKAHEAD',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_TIMEOUT',), None)

    # -- ddgs --

    _v_backend: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_BACKEND'), None)

    _v_in_url: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_IN_URL'), None)

    DEFAULT_ITEM_MATCH =\
        r'^http[s]?://dbpedia\.org/(ontology/([^a-z]\w+)|resource/(\w+))$'

    _v_item_match: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_ITEM_MATCH'), DEFAULT_ITEM_MATCH)

    DEFAULT_ITEM_SUB = r'http://dbpedia.org/\1'

    _v_item_sub: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_ITEM_SUB'), DEFAULT_ITEM_SUB)

    _v_lexeme_match: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_LEXEME_MATCH'), None)

    _v_lexeme_sub: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_LEXEME_SUB'), None)

    DEFAULT_PROPERTY_MATCH =\
        r'^http[s]?://dbpedia\.org/(ontology/[a-z]\w+)$'

    _v_property_match: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_PROPERTY_MATCH'), DEFAULT_PROPERTY_MATCH)

    DEFAULT_PROPERTY_SUB = r'http://dbpedia.org/\1'

    _v_property_sub: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_PROPERTY_SUB'), DEFAULT_PROPERTY_SUB)

    DEFAULT_SITE = 'https://dbpedia.org/'

    _v_site: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DBPEDIA_DDGS_SEARCH_SITE'), DEFAULT_SITE)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == DBpedia DDGS search ==================================================

TOptions: TypeAlias = DBpediaDDGS_SearchOptions


class DBpediaDDGS_Search(
        DDGS_Search[TOptions],
        search_name='dbpedia-ddgs',
        search_description='DBpedia DDGS search'
):
    """DBpedia DDGS search.

    Parameters:
       search_name: Name of the search plugin to instantiate.
       kwargs: Other keyword arguments.
    """

    def __init__(self, search_name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(search_name, *args, **kwargs)

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cls.get_context(context).options.search.dbpedia_ddgs

    @override
    def _lexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[DBpediaDDGS_Search.TData]:
        return iter(())

    @override
    def _alexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[DBpediaDDGS_Search.TData]:
        return self._asearch_empty_iterator()

    @override
    def _aproperty_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[DBpediaDDGS_Search.TData]:
        options.site = 'https://dbpedia.org/ontology'
        return super()._aproperty_data(search, options)
