# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import URIRef

from ..namespace import Wikidata
from .kif_object import KIF_Object


class Rank(KIF_Object):
    """Abstract base class for statement ranks."""

    preferred: 'PreferredRank'
    normal: 'NormalRank'
    deprecated: 'DeprecatedRank'

    _uri: URIRef

    @classmethod
    def _from_rdflib(cls, uri: URIRef) -> 'Rank':
        if Wikidata.is_wikibase_preferred_rank(uri):
            return cls.preferred
        elif Wikidata.is_wikibase_normal_rank(uri):
            return cls.normal
        elif Wikidata.is_wikibase_deprecated_rank(uri):
            return cls.deprecated
        else:
            raise ValueError(f'bad Wikibase rank: {uri}')

    def _to_rdflib(self) -> URIRef:
        return self._uri


class PreferredRank(Rank):
    """Represents the most important information."""

    _uri: URIRef = Wikidata.PREFERRED

    def __init__(self):
        return super().__init__()


class NormalRank(Rank):
    """Represents complementary information."""

    _uri: URIRef = Wikidata.NORMAL

    def __init__(self):
        return super().__init__()


class DeprecatedRank(Rank):
    """Represents unreliable information."""

    _uri: URIRef = Wikidata.DEPRECATED

    def __init__(self):
        return super().__init__()


Rank.deprecated = DeprecatedRank()
Rank.normal = NormalRank()
Rank.preferred = PreferredRank()

Deprecated = Rank.deprecated
Normal = Rank.normal
Preferred = Rank.preferred
