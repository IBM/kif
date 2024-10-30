# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DatatypeVariable,
    DeprecatedRank,
    IRI_Variable,
    Item,
    ItemDatatype,
    ItemVariable,
    NormalRank,
    PreferredRank,
    QuantityVariable,
    Rank,
    RankVariable,
    StatementVariable,
    Term,
    Theta,
    ValueSnakVariable,
    Variable,
)
from kif_lib.typing import assert_type, cast, Optional, Set

from ....tests import VariableTestCase


class Test(VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(RankVariable.object_class, type[Rank])
        self.assertIs(RankVariable.object_class, Rank)

    def test_check(self) -> None:
        assert_type(RankVariable.check(RankVariable('x')), RankVariable)
        assert_type(RankVariable.check(Variable('x', Rank)), RankVariable)
        self._test_check(RankVariable)

    def test__init__(self) -> None:
        assert_type(RankVariable('x'), RankVariable)
        self._test__init__(RankVariable, self.assert_rank_variable)

    def test_variables(self) -> None:
        assert_type(RankVariable('x').variables, Set[Variable])
        self._test_variables(RankVariable)

    def test_instantiate(self) -> None:
        assert_type(RankVariable('x').instantiate({}), Optional[Term])
        self.assert_preferred_rank(cast(
            PreferredRank, RankVariable('x').instantiate({
                RankVariable('x'): PreferredRank()
            })))
        self.assert_normal_rank(cast(
            NormalRank, RankVariable('x').instantiate({
                RankVariable('x'): NormalRank()
            })))
        self.assert_deprecated_rank(cast(
            DeprecatedRank, RankVariable('x').instantiate({
                RankVariable('x'): DeprecatedRank()
            })))

    def test_instantiate_and_match(self) -> None:
        assert_type(RankVariable('x').instantiate({}), Optional[Term])
        assert_type(RankVariable('x').match(Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            RankVariable,
            success=[
                RankVariable('x'),
                PreferredRank(),
                NormalRank(),
                DeprecatedRank(),
            ],
            failure=[
                DatatypeVariable('x'),
                IRI_Variable('x'),
                Item('x'),
                ItemDatatype(),
                ItemVariable('x'),
                QuantityVariable('x'),
                StatementVariable('x'),
                ValueSnakVariable('x'),
            ])


if __name__ == '__main__':
    Test.main()
