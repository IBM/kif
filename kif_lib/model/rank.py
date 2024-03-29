# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from functools import cache

from rdflib import URIRef

from ..namespace import Wikidata
from .kif_object import KIF_Object


class Rank(KIF_Object):
    """Abstract base class for statement ranks."""

    #: Preferred rank.
    preferred: 'PreferredRank'

    #: Normal rank.
    normal: 'NormalRank'

    #: Deprecated rank.
    deprecated: 'DeprecatedRank'

    _uri: URIRef

    @classmethod
    @cache
    def _from_rdflib(cls, uri: URIRef) -> 'Rank':
        if Wikidata.is_wikibase_preferred_rank(uri):
            return cls.preferred
        elif Wikidata.is_wikibase_normal_rank(uri):
            return cls.normal
        elif Wikidata.is_wikibase_deprecated_rank(uri):
            return cls.deprecated
        else:
            raise ValueError(f'bad Wikibase rank: {uri}')

    @classmethod
    def _to_rdflib(cls) -> URIRef:
        return cls._uri


class PreferredRank(Rank):
    """Most important information."""

    _uri: URIRef = Wikidata.PREFERRED

    def __init__(self):
        return super().__init__()


class NormalRank(Rank):
    """Complementary information."""

    _uri: URIRef = Wikidata.NORMAL

    def __init__(self):
        return super().__init__()


class DeprecatedRank(Rank):
    """Unreliable information."""

    _uri: URIRef = Wikidata.DEPRECATED

    def __init__(self):
        return super().__init__()


Rank.deprecated = DeprecatedRank()
Rank.normal = NormalRank()
Rank.preferred = PreferredRank()

Deprecated = Rank.deprecated
Normal = Rank.normal
Preferred = Rank.preferred
