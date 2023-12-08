# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import re
from typing import Collection, Union

from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace

from .wikibase import WIKIBASE

T_NS = Union[type[DefinedNamespace], Namespace]
T_URI = Union[URIRef, str]


class Wikidata:
    WIKIDATA = Namespace('http://www.wikidata.org/')
    P = Namespace(WIKIDATA['prop/'])
    PQ = Namespace(P['qualifier/'])
    PQN = Namespace(PQ['value-normalized/'])
    PQV = Namespace(PQ['value/'])
    PR = Namespace(P['reference/'])
    PRN = Namespace(PR['value-normalized/'])
    PRV = Namespace(PR['value/'])
    PS = Namespace(P['statement/'])
    PSN = Namespace(PS['value-normalized/'])
    PSV = Namespace(PS['value/'])
    WD = Namespace(WIKIDATA['entity/'])
    WDATA = Namespace(WIKIDATA['wiki/Special:EntityData/'])
    WDGENID = Namespace(WIKIDATA['.well-known/genid/'])
    WDNO = Namespace(P['novalue/'])
    WDREF = Namespace(WIKIDATA['reference/'])
    WDS = Namespace(WD['statement/'])
    WDT = Namespace(P['direct/'])
    WDV = Namespace(WIKIDATA['value/'])

    namespaces: dict[str, Namespace] = {
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

    prefixes: dict[str, Namespace] = {
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

    default_entity_prefixes = [WD]
    default_item_prefixes = [WD]
    default_property_prefixes = [WD]
    default_some_value_prefixes = [WDGENID]

    PREFERRED = WIKIBASE.PreferredRank
    NORMAL = WIKIBASE.NormalRank
    DEPRECATED = WIKIBASE.DeprecatedRank

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
            pfx, name = _re.match(uri).groups()
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
        return prefix in prefixes and (name[0] == 'Q' or name[0] == 'P')

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
    def is_wd_some_value(
            cls,
            uri: T_URI,
            prefixes: Collection[T_NS] = default_some_value_prefixes
    ) -> bool:
        try:
            pfx, name = cls.split_wikidata_uri(uri)
        except Exception:
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
        return uri == cls.PREFERRED

    @classmethod
    def is_wikibase_normal_rank(cls, uri: T_URI) -> bool:
        return uri == cls.NORMAL

    @classmethod
    def is_wikibase_deprecated_rank(cls, uri: T_URI) -> bool:
        return uri == cls.DEPRECATED
