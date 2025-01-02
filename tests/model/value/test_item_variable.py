# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Item, ItemVariable, Lexeme, Property, Term, Theta, Variable
from kif_lib.typing import assert_type, Optional, Set

from ...tests import EntityVariableTestCase


class Test(EntityVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(ItemVariable.object_class, type[Item])
        self.assertIs(ItemVariable.object_class, Item)

    def test_check(self) -> None:
        assert_type(ItemVariable.check(ItemVariable('x')), ItemVariable)
        assert_type(ItemVariable.check(Variable('x', Item)), ItemVariable)
        self._test_check(ItemVariable)

    def test__init__(self) -> None:
        assert_type(ItemVariable('x'), ItemVariable)
        self._test__init__(ItemVariable, self.assert_item_variable)

    def test_variables(self) -> None:
        assert_type(ItemVariable('x').variables, Set[Variable])
        self._test_variables(ItemVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(ItemVariable('x').instantiate({}), Optional[Term])
        assert_type(ItemVariable('x').match(Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            ItemVariable,
            success=[
                Item('x'),
                Item(Variable('x')),
            ],
            failure=[
                Lexeme('x'),
                Lexeme(Variable('x')),
                Property('x'),
                Property(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
