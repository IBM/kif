# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Deprecated,
    DeprecatedRank,
    Item,
    Normal,
    NormalRank,
    Preferred,
    PreferredRank,
    Rank,
    RankVariable,
    SnakSet,
    Term,
    Theta,
    Variable,
)
from kif_lib.namespace import WIKIBASE
from kif_lib.typing import assert_type, cast, Iterator, Optional, Set

from ....tests import ClosedTermTestCase


class Test(ClosedTermTestCase):

    def test_variable_class(self) -> None:
        assert_type(Rank.variable_class, type[RankVariable])
        self.assertIs(Rank.variable_class, RankVariable)

    def test_check(self) -> None:
        assert_type(Rank.check(NormalRank()), Rank)
        self._test_check(
            Rank,
            success=[
                (Deprecated, DeprecatedRank()),
                (DeprecatedRank(), Deprecated),
                (Normal, NormalRank()),
                (NormalRank(), Normal),
                (Preferred, PreferredRank()),
                (PreferredRank(), Preferred),
            ],
            failure=[0, {}, Item('x'), SnakSet()])

    def test__init__(self) -> None:
        self.assert_abstract_class(Rank)

    def test_variables(self) -> None:
        assert_type(NormalRank().variables, Set[Variable])
        self._test_variables(
            Rank,
            (PreferredRank(), set()),
            (NormalRank(), set()),
            (DeprecatedRank(), set()))

    def test_instantiate(self) -> None:
        assert_type(NormalRank().instantiate({}), Term)
        self._test_instantiate(
            Rank, success=[(NormalRank(), NormalRank(), {})])

    def test_match(self) -> None:
        assert_type(NormalRank().match(Variable('x')), Optional[Theta])

        def it_success() -> Iterator[tuple[Term, Term, Theta]]:
            for r in self.ALL_RANK_CLASSES:
                if r is not Rank:
                    yield (r(), RankVariable('x'), {RankVariable('x'): r()})
                    yield (r(), Variable('x'), {Variable('x'): r()})

        def it_failure() -> Iterator[tuple[Term, Term]]:
            for r in self.ALL_RANK_CLASSES:
                if r is Rank:
                    continue
                for v in self.ALL_VARIABLE_CLASSES:
                    if v in (RankVariable, Variable):
                        continue
                    else:
                        yield (r(), v('x'))

        self._test_match(Rank, success=it_success(), failure=it_failure())

    def test__from_rdflib(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 1, 'uri', 'cannot coerce URIRef into Rank',
            Rank._from_rdflib, WIKIBASE.Url)
        self.assert_raises_bad_argument(
            TypeError, 1, 'uri',
            'cannot coerce NormalRank into DeprecatedRank',
            DeprecatedRank._from_rdflib, WIKIBASE.NormalRank)
        self.assert_deprecated_rank(
            cast(DeprecatedRank, Rank._from_rdflib(WIKIBASE.DeprecatedRank)))
        self.assert_deprecated_rank(
            cast(DeprecatedRank, DeprecatedRank._from_rdflib(
                WIKIBASE.DeprecatedRank)))
        self.assert_normal_rank(
            cast(NormalRank, NormalRank._from_rdflib(WIKIBASE.NormalRank)))
        self.assert_preferred_rank(
            cast(PreferredRank, PreferredRank._from_rdflib(
                WIKIBASE.PreferredRank)))

    def test__to_rdflib(self) -> None:
        self.assertEqual(Deprecated._to_rdflib(), WIKIBASE.DeprecatedRank)
        self.assertEqual(Normal._to_rdflib(), WIKIBASE.NormalRank)
        self.assertEqual(Preferred._to_rdflib(), WIKIBASE.PreferredRank)


if __name__ == '__main__':
    Test.main()
