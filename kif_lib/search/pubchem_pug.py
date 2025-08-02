# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import logging

import httpx

from .. import functools
from ..context import Context
from ..model import IRI, Item, Text
from ..namespace.pubchem import PubChem
from ..typing import (
    Any,
    AsyncIterator,
    ClassVar,
    Final,
    Iterable,
    Iterator,
    override,
    TypeAlias,
)
from .httpx import HttpxSearch, HttpxSearchOptions

_logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclasses.dataclass
class PubChemPUG_SearchOptions(HttpxSearchOptions, name='pubchem_pug'):
    """PubChem PUG search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_PUBCHEM_PUG_SEARCH_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_PUBCHEM_PUG_SEARCH_MAX_LIMIT',), None)

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_PUBCHEM_PUG_SEARCH_LANGUAGE',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_PUBCHEM_PUG_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_PUBCHEM_PUG_SEARCH_LOOKAHEAD',), None)

    DEFAULT_MAX_PAGE_SIZE = 50

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_PUBCHEM_PUG_SEARCH_MAX_PAGE_SIZE',), DEFAULT_MAX_PAGE_SIZE)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_PUBCHEM_PUG_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_PUBCHEM_PUG_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_PUBCHEM_PUG_SEARCH_TIMEOUT',), None)

    # -- httpx --

    DEFAULT_IRI = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/'

    _v_iri: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_PUBCHEM_PUG_SEARCH_IRI', 'PUBCHEM_PUG'), DEFAULT_IRI)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == PubChem PUG search ====================================================

TOptions: TypeAlias = PubChemPUG_SearchOptions


class PubChemPUG_Search(
        HttpxSearch[TOptions],
        search_name='pubchem-pug',
        search_aliases=['pubchem'],
        search_description='PubChem PUG search'
):
    """PubChem PUG search.

    Parameters:
       search_name: Name of the search plugin to instantiate.
       kwargs: Other keyword arguments.
    """

    def __init__(self, search_name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(search_name, *args, **kwargs)

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cls.get_context(context).options.search.pubchem_pug

    @override
    def _to_item(self, data: PubChemPUG_Search.TData) -> Item:
        return Item(PubChem.COMPOUND[f"CID{data['CID']}"])

    @override
    def to_item_descriptor(
            self,
            data: PubChemPUG_Search.TData
    ) -> tuple[Item, Item.Descriptor]:
        item = self._to_item(data)
        if 'Synonym' in data:
            synonyms = data['Synonym']
            if synonyms:
                return item, {
                    'labels': {'en': Text(synonyms[0], 'en')},
                    'aliases': {'en': {Text(x, 'en') for x in synonyms[1:]}}}
        return item, {}

    @override
    def _item_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[PubChemPUG_Search.TData]:
        iri, timeout = self._check_options(options)
        try:
            data = self._http_get_json(
                self._build_search_iri(iri, search), timeout=timeout)
            if 'InformationList' in data:
                yield from data['InformationList'].get('Information', ())
        except httpx.HTTPStatusError as err:
            if err.response.status_code == 404:
                _logger.debug('%s', err.response.text)
            else:
                raise err

    def _check_options(
            self,
            options: TOptions
    ) -> tuple[IRI, float | None]:
        iri = options.iri
        if iri is None:
            assert self.options.DEFAULT_IRI is not None
            iri = IRI(self.options.DEFAULT_IRI)
        timeout = options.timeout
        return iri, timeout

    def _build_search_iri(
            self,
            iri: IRI,
            search: str,
    ) -> str:
        from urllib.parse import quote
        return (
            f'{iri.content}{"" if iri.content[-1] == "/" else "/"}'
            f'compound/name/{quote(search)}/synonyms/JSON')

    @override
    def _aitem_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[PubChemPUG_Search.TData]:
        return self._aitem_data_tail(search, options)

    async def _aitem_data_tail(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[PubChemPUG_Search.TData]:
        iri, timeout = self._check_options(options)
        try:
            data = await self._http_aget_json(
                self._build_search_iri(iri, search), timeout=timeout)
            if 'InformationList' in data:
                for t in data['InformationList'].get('Information', ()):
                    yield t
        except httpx.HTTPStatusError as err:
            if err.response.status_code == 404:
                _logger.debug('%s', err.response.text)
            else:
                raise err
