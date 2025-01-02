# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools

from ..rdflib import URIRef
from ..typing import (
    Any,
    cast,
    ClassVar,
    Final,
    Location,
    override,
    Self,
    TypeAlias,
    Union,
)
from .term import ClosedTerm, Term, Theta, Variable
from .value import IRI, String

TRank: TypeAlias = Union['Rank', type['Rank']]
VRank: TypeAlias = Union['RankVariable', 'Rank']
VTRank: TypeAlias = Union[Variable, TRank]


class RankVariable(Variable):
    """Rank variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Rank]]  # pyright: ignore

    @override
    def _instantiate_tail(
            self,
            theta: Theta,
            coerce: bool,
            strict: bool,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Term | None:
        obj = theta[self]
        if not strict and isinstance(obj, (IRI, String, str)):
            ###
            # IMPORTANT: We need to be able to use Wikidata datatype IRIs to
            # instantiate rank variables.
            ###
            return Rank.check(obj, function, name, position)
        else:
            return super()._instantiate_tail(
                theta, coerce, strict, function, name, position)


class Rank(ClosedTerm, variable_class=RankVariable):
    """Abstract base class for statement ranks."""

    variable_class: ClassVar[type[RankVariable]]  # pyright: ignore

    #: Singleton instance of this rank class.
    instance: ClassVar[Rank]

    def __new__(cls, rank_class: TRank | None = None):
        if rank_class is None:
            if cls is Rank:
                raise cls._check_error(
                    rank_class, cls, 'rank_class', 1)
            rank_class = cls
        elif isinstance(rank_class, Rank):
            rank_class = type(rank_class)
        if (isinstance(rank_class, type)
                and issubclass(rank_class, cls)  # pyright: ignore
                and rank_class is not Rank):
            if (hasattr(rank_class, 'instance')
                    and type(rank_class.instance) is rank_class):
                return cast(Self, rank_class.instance)
            else:
                return super().__new__(rank_class)
        else:
            raise cls._check_error(rank_class, cls, 'rank_class', 1)

    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.instance = cls()

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif (isinstance(arg, type)
              and issubclass(arg, cls)
              and arg is not Rank):
            return cast(Self, arg.instance)
        elif isinstance(arg, (IRI, String, str)):
            iri = IRI.check(arg, function, name, position)
            try:
                return cls._from_rdflib(iri.content)
            except TypeError as err:
                raise cls._check_error(
                    arg, function, name, position) from err
        else:
            raise cls._check_error(arg, function, name, position)

    @classmethod
    @functools.cache
    def _from_rdflib(cls, uri: URIRef | str) -> Self:
        from ..namespace import Wikidata
        if Wikidata.is_wikibase_preferred_rank(uri):
            res: Rank = PreferredRank()
        elif Wikidata.is_wikibase_normal_rank(uri):
            res = NormalRank()
        elif Wikidata.is_wikibase_deprecated_rank(uri):
            res = DeprecatedRank()
        else:
            raise cls._check_error(uri, cls._from_rdflib, 'uri', 1)
        return cls.check(res, cls._from_rdflib, 'uri', 1)

    def _to_rdflib(self) -> URIRef:
        from ..namespace import Wikidata
        if isinstance(self, PreferredRank):
            return Wikidata.PREFERRED
        elif isinstance(self, NormalRank):
            return Wikidata.NORMAL
        elif isinstance(self, DeprecatedRank):
            return Wikidata.DEPRECATED
        else:
            raise self._should_not_get_here()

    def __init__(self, rank_class: TRank | None = None) -> None:
        assert not (type(self) is Rank and rank_class is None)
        super().__init__()


class PreferredRank(Rank):
    """Most important information."""

    instance: ClassVar[PreferredRank]  # pyright: ignore


class NormalRank(Rank):
    """Complementary information."""

    instance: ClassVar[NormalRank]  # pyright: ignore


class DeprecatedRank(Rank):
    """Unreliable information."""

    instance: ClassVar[DeprecatedRank]  # pyright: ignore


#: Alias of singleton instance of :class:`PreferredRank`.
Preferred: Final[PreferredRank] = PreferredRank()

#: Alias of singleton instance of :class:`NormalRank`.
Normal: Final[NormalRank] = NormalRank()

#: Alias of singleton instance of :class:`DeprecatedRank`.
Deprecated: Final[DeprecatedRank] = DeprecatedRank()
