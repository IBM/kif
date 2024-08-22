# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    Item,
    ItemTemplate,
    ItemVariable,
    Lexeme,
    Quantity,
    Term,
    Variable,
)
from kif_lib.typing import assert_type, Optional

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

    def test_instantiate(self) -> None:
        assert_type(ItemVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            ItemVariable,
            success=[
                Item('x'),
                ItemTemplate(Variable('x')),
            ],
            failure=[
                IRI('x'),
                IRI.template_class(Variable('x')),
                Lexeme('x'),
                Lexeme.template_class(Variable('x')),
                Quantity(0),
                Quantity.template_class(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
