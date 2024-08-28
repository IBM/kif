# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools

from ...rdflib import URIRef
from ...typing import Self
from ..kif_object import KIF_Object


class Rank(KIF_Object):
    """Abstract base class for statement ranks."""

    @classmethod
    @functools.cache
    def _from_rdflib(cls, uri: URIRef | str) -> Self:
        from ...namespace import Wikidata
        if Wikidata.is_wikibase_preferred_rank(uri):
            res: Rank = Preferred
        elif Wikidata.is_wikibase_normal_rank(uri):
            res = Normal
        elif Wikidata.is_wikibase_deprecated_rank(uri):
            res = Deprecated
        else:
            raise cls._check_error(uri, cls._from_rdflib, 'uri', 1)
        return cls.check(res, cls._from_rdflib, 'uri', 1)

    def _to_rdflib(self) -> URIRef:
        from ...namespace import Wikidata
        if isinstance(self, PreferredRank):
            return Wikidata.PREFERRED
        elif isinstance(self, NormalRank):
            return Wikidata.NORMAL
        elif isinstance(self, DeprecatedRank):
            return Wikidata.DEPRECATED
        else:
            raise self._should_not_get_here()


class PreferredRank(Rank):
    """Most important information."""

    def __init__(self) -> None:
        super().__init__()


class NormalRank(Rank):
    """Complementary information."""

    def __init__(self) -> None:
        super().__init__()


class DeprecatedRank(Rank):
    """Unreliable information."""

    def __init__(self) -> None:
        super().__init__()


#: Preferred rank.
Preferred = PreferredRank()

#: Normal rank.
Normal = NormalRank()

#: Deprecated rank.
Deprecated = DeprecatedRank()
