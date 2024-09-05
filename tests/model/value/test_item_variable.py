# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    EntityVariable,
    IRI,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    Lexeme,
    NoValueSnak,
    Property,
    Quantity,
    SnakVariable,
    Term,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

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

    def test_instantiate(self) -> None:
        assert_type(ItemVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            ItemVariable,
            success_auto=[
                Item('x'),
                ItemTemplate(Variable('x')),
            ],
            failure_auto=[
                IRI('x'),
                IRI.template_class(Variable('x')),
                Lexeme('x'),
                Lexeme.template_class(Variable('x')),
                Quantity(0),
                Quantity.template_class(Variable('x')),
            ])

    def test_match(self) -> None:
        assert_type(ItemVariable('x').match(Item('x')), Optional[Theta])
        self._test_match(
            ItemVariable,
            success=[
                (ItemVariable('x'),
                 Item('x'),
                 {ItemVariable('x'): Item('x')}),
            ],
            failure=[
                (ItemVariable('x'), Property('y')),
                (ItemVariable('x'), IRI('x')),
            ])

    def test_unify(self) -> None:
        assert_type(ItemVariable('x').unify(Variable('x')), Optional[Theta])
        self._test_unify(
            ItemVariable,
            success=[
                (ItemVariable('x'),
                 Item(Variable('x')),
                 {ItemVariable('x'): Item(IRI_Variable('x'))}),
                (ItemVariable('x'),
                 ItemVariable('y'),
                 {ItemVariable('x'): ItemVariable('y')}),
                (ItemVariable('x'),
                 EntityVariable('y'),
                 {EntityVariable('y'): ItemVariable('x')})
            ],
            failure=[
                (ItemVariable('x'), IRI('y')),
                (ItemVariable('x'), SnakVariable('y')),
                (ItemVariable('x'), NoValueSnak(Variable('y'))),
            ])


if __name__ == '__main__':
    Test.main()
