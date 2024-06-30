# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import decimal

from kif_lib import (
    IRI,
    Item,
    ItemTemplate,
    ItemVariable,
    KIF_Object,
    Quantity,
    QuantityTemplate,
    QuantityVariable,
    String,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_DeepDataValueTemplateTestCase


class Test(kif_DeepDataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(QuantityTemplate.object_class, type[Quantity])
        self.assertIs(QuantityTemplate.object_class, Quantity)

    def test_check(self) -> None:
        assert_type(
            QuantityTemplate.check(QuantityTemplate(Variable('x'))),
            QuantityTemplate)
        self._test_check(QuantityTemplate, failure=[Quantity(0)])

    def test__init__(self) -> None:
        assert_type(QuantityTemplate(Variable('x')), QuantityTemplate)
        self._test__init__(
            QuantityTemplate,
            self.assert_quantity_template,
            success=[
                ([Variable('x')], QuantityTemplate(QuantityVariable('x'))),
                ([0, Variable('y')], Quantity(0, ItemVariable('y'))),
                ([0, Item(Variable('y'))],
                 Quantity(0, ItemTemplate(Variable('y', IRI)))),
                ([0, Item(IRI(Variable('y')))],
                 Quantity(0, ItemTemplate(IRI(Variable('y', String))))),
                ([0, None, Variable('x')],
                 Quantity(0, None, QuantityVariable('x'))),
                ([0, None, Quantity(1, Item('x')), Variable('x')],
                 Quantity(0, None, 1, QuantityVariable('x'))),
                ([Variable('x'), Variable('y'), Variable('z'), Variable('w')],
                 Quantity(
                     QuantityVariable('x'),
                     ItemVariable('y'),
                     QuantityVariable('z'),
                     QuantityVariable('w'))),
                ([Variable('x', Quantity), None, None, None],
                 Quantity(Variable('x'))),
                ([decimal.Decimal('0.1'),
                  Item(Variable('x', IRI)), None, None],
                 Quantity('0.1', Item(Variable('x')))),
                ([decimal.Decimal(0),
                  ItemTemplate(IRI(Variable('x', String)))],
                 Quantity(0, Item(IRI(Variable('x', String))))),
                ([decimal.Decimal('1.0'), None, Variable('x', Quantity), None],
                 Quantity(1.0, None, Variable('x'))),
                ([decimal.Decimal(0), None,
                  decimal.Decimal(0), Variable('x', Quantity)],
                 Quantity(0, None, 0, Variable('x'))),
            ],
            failure=[
                [0, None, None, Quantity(Variable('x'))],
                [0, None, Quantity(Variable('x'))],
                [ItemVariable('x')],
                [None, None, ItemVariable('x')],
                [None, None, None, Item(IRI(Variable('x')))],
                [None, Variable('x', IRI)],
                [Quantity(0, Variable('x'))],
                [Quantity(Variable('x'))],
            ],
            normalize=[
                [0, Item('x')],
                [0, None, 1, 2],
                [0, None, 1],
                [0, None, None, 2],
                [0, None, None, None],
                [0],
            ])

    def test_instantiate(self) -> None:
        assert_type(
            QuantityTemplate(Variable('x')).instantiate({}), KIF_Object)
        self._test_instantiate(
            QuantityTemplate,
            success=[
                (QuantityTemplate(Variable('x')),
                 Quantity(0),
                 {QuantityVariable('x'): Quantity(0)}),
                (Quantity(0, Variable('x')),
                 Quantity(0, Item(Variable('x', IRI))),
                 {ItemVariable('x'): Item(Variable('x'))}),
                (Quantity(0, None, Variable('x')),
                 Quantity(0, None, 8),
                 {QuantityVariable('x'): Quantity(8, Item('x'))}),
                (Quantity(0, None, 8, Variable('x')),
                 Quantity(0, None, 8, 9),
                 {QuantityVariable('x'): Quantity(9, Item('x'))}),
            ],
            failure=[
                (Quantity(Variable('x')),
                 {QuantityVariable('x'): Item('y')}),
            ])


if __name__ == '__main__':
    Test.main()
