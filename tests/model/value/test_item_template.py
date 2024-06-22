# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    KIF_Object,
    Lexeme,
    String,
    StringTemplate,
    StringVariable,
    TextTemplate,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_TemplateTestCase


class Test(kif_TemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(ItemTemplate.object_class, type[Item])

    def test_check(self) -> None:
        assert_type(
            ItemTemplate.check(ItemTemplate(Variable('x'))),
            ItemTemplate)
        self._test_check(
            ItemTemplate,
            success=[
                ItemTemplate(Variable('x')),
            ],
            failure=[
                Item('x'),
                ItemTemplate('x'),
                TextTemplate(Variable('x')),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(ItemTemplate(Variable('x')), ItemTemplate)
        self._test__init__(
            ItemTemplate,
            lambda x, *y: self.assert_item_template(x, *y),
            success=[
                [IRI_Template(Variable('x'))],
                [IRI_Variable('x')],
                [Variable('x', IRI)],
            ],
            normalize=[
                [IRI('x')],
                [Item(IRI('x'))],
                [String('x')],
            ],
            failure=[
                [Item(IRI(Variable('x')))],
                [ItemTemplate(Variable('x'))],
                [ItemVariable('x')],
                [Lexeme('x')],
                [TextTemplate(Variable('x'))],
            ])

    def test_instantiate(self) -> None:
        assert_type(ItemTemplate(Variable('x')).instantiate({}), KIF_Object)
        self._test_instantiate(
            ItemTemplate,
            success=[
                (ItemTemplate(Variable('x')),
                 Item('x'),
                 {IRI_Variable('x'): IRI('x')}),
                (ItemTemplate(Variable('x')),
                 ItemTemplate(Variable('y')),
                 {IRI_Variable('x'): IRI_Variable('y')}),
            ],
            failure=[
                (ItemTemplate(Variable('x')),
                 {IRI_Variable('x'): Item('x')}),
                (ItemTemplate(Variable('x')),
                 {IRI_Variable('x'): String('x')}),
                (ItemTemplate(Variable('x')),
                 {IRI_Variable('x'): StringVariable('x')}),
                (ItemTemplate(Variable('x')),
                 {IRI_Variable('x'): StringTemplate('x')}),
            ])


if __name__ == '__main__':
    Test.main()
