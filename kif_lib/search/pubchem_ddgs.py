# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import re

from ..context import Context
from ..model import Item, Text
from ..namespace.pubchem import PubChem
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
class PubChemDDGS_SearchOptions(DDGS_SearchOptions, name='pubchem_ddgs'):
    """PubChem DDGS search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_MAX_LIMIT',), None)

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_LANGUAGE',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_LOOKAHEAD',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_TIMEOUT',), None)

    # -- ddgs --

    _v_backend: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_BACKEND'), None)

    DEFAULT_ITEM_MATCH =\
        r'^http[s]?://pubchem\.ncbi\.nlm\.nih\.gov/compound/.*$'

    _v_item_match: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_ITEM_MATCH'), DEFAULT_ITEM_MATCH)

    _v_item_sub: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_ITEM_SUB'), None)

    _v_lexeme_match: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_LEXEME_MATCH'), None)

    _v_lexeme_sub: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_LEXEME_SUB'), None)

    _v_property_match: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_PROPERTY_MATCH'), None)

    _v_property_sub: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_PROPERTY_SUB'), None)

    DEFAULT_SITE = 'https://pubchem.ncbi.nlm.nih.gov/compound/'

    _v_site: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_PUBCHEM_DDGS_SEARCH_SITE'), DEFAULT_SITE)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == PubChem DDGS search ==================================================

TOptions: TypeAlias = PubChemDDGS_SearchOptions


class PubChemDDGS_Search(
        DDGS_Search[TOptions],
        search_name='pubchem-ddgs',
        search_description='PubChem DDGS search'
):
    """PubChem DDGS search.

    Parameters:
       search_name: Name of the search plugin to instantiate.
       kwargs: Other keyword arguments.
    """

    def __init__(self, search_name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(search_name, *args, **kwargs)

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cls.get_context(context).options.search.pubchem_ddgs

    _re_item_title: re.Pattern[str] = re.compile(
        r'^([^|]*)\s+\|\s+([^|]*)\s+\|\s+CID\s+(\d+).*$')

    @override
    def _to_item(self, data: DDGS_Search.TData) -> Item:
        m = self._re_item_title.match(data['title'])
        if m is not None:
            return Item(PubChem.COMPOUND['CID' + m.group(3)])
        else:
            raise ValueError(data['title'])

    @override
    def _to_item_descriptor(
            self,
            data: DDGS_Search.TData
    ) -> tuple[Item, Item.Descriptor]:
        m = self._re_item_title.match(data['title'])
        if m is not None:
            label, alias, cid, _ = m.groups()
            return (Item(PubChem.COMPOUND['CID' + cid]), {
                'labels': {'en': Text(label, 'en')},
                'aliases': {'en': {Text(alias, 'en')}}})
        else:
            raise ValueError(data['title'])

    @override
    def _lexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[PubChemDDGS_Search.TData]:
        return iter(())

    @override
    def _alexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[PubChemDDGS_Search.TData]:
        return self._asearch_empty_iterator()

    @override
    def _property_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[PubChemDDGS_Search.TData]:
        return iter(())

    @override
    def _aproperty_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[PubChemDDGS_Search.TData]:
        return self._asearch_empty_iterator()
