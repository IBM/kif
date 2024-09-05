# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    IRI,
    IRI_Variable,
    Item,
    ItemTemplate,
    Lexeme,
    Property,
    Quantity,
    Term,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import EntityTemplateTestCase


class Test(EntityTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(ItemTemplate.object_class, type[Item])
        self.assertIs(ItemTemplate.object_class, Item)

    def test_check(self) -> None:
        assert_type(
            ItemTemplate.check(ItemTemplate(Variable('x'))),
            ItemTemplate)
        self._test_check(ItemTemplate)

    def test__init__(self) -> None:
        assert_type(ItemTemplate(Variable('x')), ItemTemplate)
        self._test__init__(
            ItemTemplate,
            self.assert_item_template,
            failure=[
                [Lexeme('x')],
                [Property('x')],
            ])

    def test_variables(self) -> None:
        assert_type(ItemTemplate(Variable('x')).variables, Set[Variable])
        self._test_variables(ItemTemplate)

    def test_instantiate(self) -> None:
        assert_type(ItemTemplate(Variable('x')).instantiate({}), Term)
        self._test_instantiate(ItemTemplate)

    def test_match(self) -> None:
        assert_type(
            ItemTemplate(Variable('x')).match(Item('x')), Optional[Theta])
        self._test_match(
            ItemTemplate,
            success=[
                (Item(Variable('x')),
                 Item('x'),
                 {IRI_Variable('x'): IRI('x')}),
            ],
            failure=[
                (Item(Variable('x')), Property('x')),
                (Item(Variable('x')), Lexeme('x')),
                (Item(Variable('x')), Quantity(0)),
            ])

    def test_unify(self) -> None:
        assert_type(
            ItemTemplate(Variable('x')).unify(Variable('x')), Optional[Theta])
        self._test_unify(ItemTemplate)


if __name__ == '__main__':
    Test.main()
