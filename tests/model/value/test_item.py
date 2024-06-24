# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Item,
    ItemDatatype,
    Items,
    ItemTemplate,
    ItemVariable,
    Lexeme,
    Property,
    Text,
    Variable,
)
from kif_lib.typing import assert_type, Iterable

from ...tests import kif_EntityTestCase


class Test(kif_EntityTestCase):

    def test_datatype_class(self) -> None:
        assert_type(Item.datatype_class, type[ItemDatatype])

    def test_datatype(self) -> None:
        assert_type(Item.datatype, ItemDatatype)
        self.assertIsInstance(Item.datatype, ItemDatatype)

    def test_template_class(self) -> None:
        assert_type(Item.template_class, type[ItemTemplate])

    def test_variable_class(self) -> None:
        assert_type(Item.variable_class, type[ItemVariable])

    def test_check(self) -> None:
        assert_type(Item.check(Item('x')), Item)
        self._test_check(
            Item,
            success=[
                ('abc', Item('abc')),
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
