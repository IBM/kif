# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import functools
import logging

from ..context import Context
from ..model import Entity, IRI, Item, KIF_Object, Lexeme, Property, T_IRI
from ..typing import (
    Any,
    ClassVar,
    Final,
    Iterable,
    Iterator,
    Literal,
    Mapping,
    override,
    TypeAlias,
)
from .httpx import HttpxSearch, HttpxSearchOptions

_logger: Final[logging.Logger] = logging.getLogger(__name__)


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
    def _item_metadata(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[tuple[Item, WikidataSearch.TMetadata]]:
        return self._x_metadata('item', search, options)  # type: ignore

    @override
    def _property_metadata(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[tuple[Property, WikidataSearch.TMetadata]]:
        return self._x_metadata('property', search, options)  # type: ignore

    @override
    def _lexeme_metadata(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[tuple[Lexeme, WikidataSearch.TMetadata]]:
        return self._x_metadata('lexeme', search, options)  # type: ignore

    def _x_metadata(
            self,
            type: Literal['item', 'lexeme', 'property'],
            search: str,
            options: TOptions
    ) -> Iterator[tuple[Entity, WikidataSearch.TMetadata]]:
        iri = options.iri
        if iri is None:
            assert self.options.DEFAULT_IRI is not None
            iri = IRI(self.options.DEFAULT_IRI)
        language = options.language
        assert language is not None
        limit = options.limit
        if limit is None:
            limit = options.max_limit
        assert limit is not None
        page_size = min(options.page_size, options.max_page_size)
        get_json = functools.partial(
            self._http_get_json, iri.content)
        mk_params = functools.partial(
            self._build_search_entities_params,
            search, type, 'json', options.language, page_size)
        parse = functools.partial(
            self._parse_search_entities_results_entry, type)
        count, offset = 0, 0
        while count < limit:
            res = get_json(mk_params(offset))
            try:
                for t in res['search']:
                    yield parse(t)
                    count += 1
                    if count == limit:
                        break
                if len(res['search']) < page_size:
                    break
                offset += page_size
            except KeyError as err:
                _logger.error('bad wbsearchentities response: %s', res)
                raise self.Error(err) from err

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

    def _parse_search_entities_results_entry(
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
