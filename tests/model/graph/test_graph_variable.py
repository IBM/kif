# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Graph,
    GraphVariable,
    Item,
    Lexeme,
    PreferredRank,
    Property,
    ReferenceRecordSet,
    SnakSet,
    Term,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(GraphVariable.object_class, type[Graph])
        self.assertIs(GraphVariable.object_class, Graph)

    def test_check(self) -> None:
        assert_type(
            GraphVariable.check(GraphVariable('x')), GraphVariable)
        assert_type(
            GraphVariable.check(Variable('x', Graph)), GraphVariable)
        self._test_check(GraphVariable)

    def test__init__(self) -> None:
        assert_type(GraphVariable('x'), GraphVariable)
        self._test__init__(
            GraphVariable, self.assert_graph_variable)

    def test_variables(self) -> None:
        assert_type(GraphVariable('x').variables, Set[Variable])
        self._test_variables(GraphVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(GraphVariable('x').instantiate({}), Optional[Term])
        assert_type(GraphVariable('x').match(SnakSet()), Optional[Theta])
        self._test_instantiate_and_match(
            GraphVariable,
            success=[
                Graph(),
                GraphVariable('x'),
                Graph(Property('x')(Item('y'), Item('z'))),
                Graph(Property('x')(Item('y'), 0),
                      Property('y')(Lexeme('z'), 1, rank=PreferredRank())),
            ],
            failure=[
                Item('x'),
                Property('x').some_value(),
                ReferenceRecordSet(),
                SnakSet(),
            ])


if __name__ == '__main__':
    Test.main()
