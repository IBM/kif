# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re

from ..rdflib import DefinedNamespace, Namespace, URIRef
from ..typing import Collection, Final, TypeAlias, Union
from .wikibase import WIKIBASE

T_NS: TypeAlias = Union[type[DefinedNamespace], Namespace]
T_URI: TypeAlias = Union[URIRef, str]


class Wikidata:
    """The Wikidata namespace."""

    WIKIDATA: Final[Namespace] = Namespace('http://www.wikidata.org/')
    P: Final[Namespace] = Namespace(WIKIDATA['prop/'])
    PQ: Final[Namespace] = Namespace(P['qualifier/'])
    PQN: Final[Namespace] = Namespace(PQ['value-normalized/'])
    PQV: Final[Namespace] = Namespace(PQ['value/'])
    PR: Final[Namespace] = Namespace(P['reference/'])
    PRN: Final[Namespace] = Namespace(PR['value-normalized/'])
    PRV: Final[Namespace] = Namespace(PR['value/'])
    PS: Final[Namespace] = Namespace(P['statement/'])
    PSN: Final[Namespace] = Namespace(PS['value-normalized/'])
    PSV: Final[Namespace] = Namespace(PS['value/'])
    WD: Final[Namespace] = Namespace(WIKIDATA['entity/'])
    WDATA: Final[Namespace] = Namespace(WIKIDATA['wiki/Special:EntityData/'])
    WDGENID: Final[Namespace] = Namespace(WIKIDATA['.well-known/genid/'])
    WDNO: Final[Namespace] = Namespace(P['novalue/'])
    WDREF: Final[Namespace] = Namespace(WIKIDATA['reference/'])
    WDS: Final[Namespace] = Namespace(WD['statement/'])
    WDT: Final[Namespace] = Namespace(P['direct/'])
    WDV: Final[Namespace] = Namespace(WIKIDATA['value/'])

    namespaces: Final[dict[str, Namespace]] = {
        str(WIKIDATA): WIKIDATA,
        str(P): P,
        str(PQ): PQ,
        str(PQN): PQN,
        str(PQV): PQV,
        str(PR): PR,
        str(PRN): PRN,
        str(PRV): PRV,
        str(PS): PS,
        str(PSN): PSN,
        str(PSV): PSV,
        str(WD): WD,
        str(WDATA): WDATA,
        str(WDGENID): WDGENID,
        str(WDNO): WDNO,
        str(WDREF): WDREF,
        str(WDS): WDS,
        str(WDT): WDT,
        str(WDV): WDV,
    }

    schema: Final[dict[str, Namespace]] = {
        'p': P,
        'pq': PQ,
        'pqv': PQV,
        'pr': PR,
        'prv': PRV,
        'ps': PS,
        'psv': PSV,
        'wdno': WDNO,
        'wdt': WDT,
    }

    prefixes: Final[dict[str, Namespace]] = {
        'wikidata': WIKIDATA,
        'p': P,
        'pq': PQ,
        'pqn': PQN,
        'pqv': PQV,
        'pr': PR,
        'prn': PRN,
        'prv': PRV,
        'ps': PS,
        'psn': PSN,
        'psv': PSV,
        'wd': WD,
        'wdata': WDATA,
        'wdgenid': WDGENID,
        'wdno': WDNO,
        'wdref': WDREF,
        'wds': WDS,
        'wdt': WDT,
        'wdv': WDV,
    }

    default_entity_prefixes: Final[Collection[T_NS]] = (WD,)
    default_item_prefixes: Final[Collection[T_NS]] = (WD,)
    default_property_prefixes: Final[Collection[T_NS]] = (WD,)
    default_lexeme_prefixes: Final[Collection[T_NS]] = (WD,)
    default_some_value_prefixes: Final[Collection[T_NS]] = (WDGENID,)

    PREFERRED: Final[URIRef] = WIKIBASE.PreferredRank
    NORMAL: Final[URIRef] = WIKIBASE.NormalRank
    DEPRECATED: Final[URIRef] = WIKIBASE.DeprecatedRank

    @classmethod
    def is_wikidata_uri(cls, uri: T_URI) -> bool:
        return uri.startswith(cls.WIKIDATA)

    @classmethod
    def split_wikidata_uri(
            cls,
            uri: T_URI,
            _re=re.compile(r'^(.*/)([^/]*)$')
    ) -> tuple[T_NS, str]:
        if cls.is_wikidata_uri(uri):
            m = _re.match(uri)
            assert m is not None
            pfx, name = m.groups()
            return cls.namespaces[pfx], name
        else:
            raise ValueError(f'bad Wikidata URI: {uri}')

    @classmethod
    def get_wikidata_namespace(cls, uri: T_URI) -> T_NS:
        return cls.split_wikidata_uri(uri)[0]

    @classmethod
    def get_wikidata_name(cls, uri: T_URI) -> str:
        return cls.split_wikidata_uri(uri)[1]

    @classmethod
    def is_wd_entity(
            cls,
            uri: T_URI,
            prefixes: Collection[T_NS] = default_entity_prefixes
    ) -> bool:
        try:
            pfx, name = cls.split_wikidata_uri(uri)
        except ValueError:
            return False
        else:
            return cls._is_wd_entity(pfx, name, prefixes)

    @classmethod
    def _is_wd_entity(
            cls,
            prefix: T_NS,
            name: str,
            prefixes: Collection[T_NS]
    ) -> bool:
        return prefix in prefixes and name[0] in 'QPL'

    @classmethod
    def is_wd_item(
            cls,
            uri: T_URI,
            prefixes: Collection[T_NS] = default_item_prefixes
    ) -> bool:
        try:
            pfx, name = cls.split_wikidata_uri(uri)
        except ValueError:
            return False
        else:
            return cls._is_wd_item(pfx, name, prefixes)

    @classmethod
    def _is_wd_item(
            cls,
            prefix: T_NS,
            name: str,
            prefixes: Collection[T_NS]
    ) -> bool:
        return prefix in prefixes and name[0] == 'Q'

    @classmethod
    def is_wd_property(
            cls,
            uri: T_URI,
            prefixes: Collection[T_NS] = default_property_prefixes
    ) -> bool:
        try:
            pfx, name = cls.split_wikidata_uri(uri)
        except ValueError:
            return False
        else:
            return cls._is_wd_property(pfx, name, prefixes)

    @classmethod
    def _is_wd_property(
            cls,
            prefix: T_NS,
            name: str,
            prefixes: Collection[T_NS]
    ) -> bool:
        return prefix in prefixes and name[0] == 'P'

    @classmethod
    def is_wd_lexeme(
            cls,
            uri: T_URI,
            prefixes: Collection[T_NS] = default_lexeme_prefixes
    ) -> bool:
        try:
            pfx, name = cls.split_wikidata_uri(uri)
        except ValueError:
            return False
        else:
            return cls._is_wd_lexeme(pfx, name, prefixes)

    @classmethod
    def _is_wd_lexeme(
            cls,
            prefix: T_NS,
            name: str,
            prefixes: Collection[T_NS]
    ) -> bool:
        return prefix in prefixes and name[0] == 'L'

    @classmethod
    def is_wd_some_value(
            cls,
            uri: T_URI,
            prefixes: Collection[T_NS] = default_some_value_prefixes
    ) -> bool:
        try:
            pfx, name = cls.split_wikidata_uri(uri)
        except ValueError:
            return False
        else:
            return cls._is_wd_some_value(pfx, name, prefixes)

    @classmethod
    def _is_wd_some_value(
            cls,
            prefix: T_NS,
            name: str,
            prefixes: Collection[T_NS]
    ) -> bool:
        return prefix in prefixes

    @classmethod
    def is_wikibase_preferred_rank(cls, uri: T_URI) -> bool:
        return str(uri) == str(cls.PREFERRED)

    @classmethod
    def is_wikibase_normal_rank(cls, uri: T_URI) -> bool:
        return str(uri) == str(cls.NORMAL)

    @classmethod
    def is_wikibase_deprecated_rank(cls, uri: T_URI) -> bool:
        return str(uri) == str(cls.DEPRECATED)
