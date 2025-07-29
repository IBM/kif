# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Item, ItemTemplate, Lexeme, Property, Term, Theta, Variable
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

    def test_replace(self) -> None:
        self.assertEqual(
            ItemTemplate(Variable('x')).replace(Variable('y')),
            ItemTemplate(Variable('y')))
        self.assertEqual(
            ItemTemplate(Variable('x')).replace(iri=Variable('y')),
            ItemTemplate(Variable('y')))
        self.assertEqual(
            ItemTemplate(Variable('x')).replace(ItemTemplate.KEEP),
            ItemTemplate(Variable('x')))
        self.assertEqual(
            ItemTemplate(Variable('x')).replace(iri=ItemTemplate.KEEP),
            ItemTemplate(Variable('x')))
        # item
        self.assertEqual(
            ItemTemplate(Variable('x')).replace('x'), Item('x'))
        self.assertEqual(
            ItemTemplate(Variable('x')).replace(iri='x'), Item('x'))

    def test_variables(self) -> None:
        assert_type(ItemTemplate(Variable('x')).variables, Set[Variable])
        self._test_variables(ItemTemplate)

    def test_instantiate(self) -> None:
        assert_type(ItemTemplate(Variable('x')).instantiate({}), Term)
        self._test_instantiate(ItemTemplate)

    def test_match(self) -> None:
        assert_type(
            ItemTemplate(Variable('x')).match(Variable('x')), Optional[Theta])
        self._test_match(ItemTemplate)


if __name__ == '__main__':
    Test.main()
