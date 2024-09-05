# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    Item,
    ItemDatatype,
    Items,
    ItemTemplate,
    ItemVariable,
    Lexeme,
    Property,
    Term,
    Text,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Iterable, Optional, Set

from ...tests import EntityTestCase


class Test(EntityTestCase):

    def test_datatype_class(self) -> None:
        assert_type(Item.datatype_class, type[ItemDatatype])
        self.assertIs(Item.datatype_class, ItemDatatype)

    def test_datatype(self) -> None:
        assert_type(Item.datatype, ItemDatatype)
        self.assert_item_datatype(Item.datatype)

    def test_template_class(self) -> None:
        assert_type(Item.template_class, type[ItemTemplate])
        self.assertIs(Item.template_class, ItemTemplate)

    def test_variable_class(self) -> None:
        assert_type(Item.variable_class, type[ItemVariable])
        self.assertIs(Item.variable_class, ItemVariable)

    def test_check(self) -> None:
        assert_type(Item.check(Item('x')), Item)
        self._test_check(
            Item,
            success=[
                ('x', Item('x')),
                (ExternalId('x'), Item('x')),
            ],
            failure=[
                ItemTemplate(Variable('x')),
                Lexeme('x'),
                Property('x'),
                Text('x'),
                Variable('x', Text)
            ])

    def test__init__(self) -> None:
        assert_type(Item('x'), Item)
        self._test__init__(
            Item,
            self.assert_item,
            failure=[
                [ItemTemplate(Variable('x'))],
                [Lexeme('x')],
                [Property('x')],
                [Text('x')],
                [Variable('x', Text)],
            ])

    def test_variables(self) -> None:
        assert_type(Item('x').variables, Set[Variable])
        self._test_variables(Item)

    def test_instantiate(self) -> None:
        assert_type(Item('x').instantiate({}), Term)
        self._test_instantiate(Item)

    def test_match(self) -> None:
        assert_type(Item('x').match(Item('x')), Optional[Theta])
        self._test_match(Item)

    def test_unify(self) -> None:
        assert_type(Item('x').unify(Variable('x')), Optional[Theta])
        self._test_unify(Item)

    def test_Items(self) -> None:
        assert_type(Items('a', 'b', 'c'), Iterable[Item])
        self._test_Entities(
            Items,
            self.assert_item,
            failure=[
                Item('x'),
                ItemTemplate(Variable('x')),
                Lexeme('x'),
                Property('x'),
                Text('x'),
                Variable('x', Text),
            ])


if __name__ == '__main__':
    Test.main()
