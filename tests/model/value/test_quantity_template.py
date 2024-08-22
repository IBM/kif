# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import decimal

from kif_lib import (
    DataValue,
    DeepDataValue,
    IRI,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    Quantity,
    QuantityTemplate,
    QuantityVariable,
    String,
    Term,
    Variable,
)
from kif_lib.typing import assert_type, cast

from ...tests import DeepDataValueTemplateTestCase


class Test(DeepDataValueTemplateTestCase):

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

        # extra
        x = Variable('x')
        self.assert_raises_bad_argument(
            ValueError, 1, None, 'cannot coerce str into Quantity',
            (QuantityTemplate, 'Quantity'), 'x')
        self.assert_raises_bad_argument(
            TypeError, 2, None, 'cannot coerce int into IRI',
            (QuantityTemplate, 'Quantity'), 0, 0)
        self.assert_raises_bad_argument(
            ValueError, 3, None, 'cannot coerce str into Quantity',
            (QuantityTemplate, 'Quantity'), 0, None, 'x')
        self.assert_raises_bad_argument(
            ValueError, 4, None, 'cannot coerce str into Quantity',
            (QuantityTemplate, 'Quantity'), 0, None, None, 'x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into QuantityVariable",
            QuantityTemplate, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce QuantityTemplate into Quantity',
            QuantityTemplate, QuantityTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            "cannot coerce IRI_Variable into ItemVariable",
            QuantityTemplate, 0, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 3, None,
            "cannot coerce IRI_Variable into QuantityVariable",
            QuantityTemplate, 0, None, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 3, None,
            'cannot coerce QuantityTemplate into Quantity',
            QuantityTemplate, 0, None, QuantityTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 4, None,
            "cannot coerce IRI_Variable into QuantityVariable",
            QuantityTemplate, 0, None, None, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 4, None,
            'cannot coerce QuantityTemplate into Quantity',
            QuantityTemplate, 0, None, None, QuantityTemplate(Variable('x')))
        self.assert_quantity_template(
            QuantityTemplate(x),
            QuantityVariable('x'), None, None, None)
        self.assert_quantity_template(
            QuantityTemplate(0, x), decimal.Decimal(0),
            ItemVariable('x'), None, None)
        self.assert_quantity_template(
            QuantityTemplate(0, None, x),
            decimal.Decimal(0), None, QuantityVariable('x'), None)
        self.assert_quantity_template(
            QuantityTemplate(0, None, None, x),
            decimal.Decimal(0), None, None, QuantityVariable('x'))
        self.assert_quantity_template(
            QuantityTemplate(
                Variable('x'),
                Variable('y'),
                Variable('z'),
                Variable('w')),
            QuantityVariable('x'),
            ItemVariable('y'),
            QuantityVariable('z'),
            QuantityVariable('w'))
        self.assert_quantity_template(
            Quantity(x), Variable('x', Quantity), None, None, None)
        self.assert_quantity_template(
            Quantity(0, Item(x)), decimal.Decimal(0),
            Item(Variable('x', IRI)), None, None)
        self.assert_quantity_template(
            Quantity(0, Item(IRI(x))), decimal.Decimal(0),
            ItemTemplate(IRI(Variable('x', String))), None, None)
        self.assert_quantity_template(
            Quantity(0, None, x), decimal.Decimal(0),
            None, Variable('x', Quantity), None)
        self.assert_quantity_template(
            Quantity(0, None, 0, x),
            decimal.Decimal(0), None,
            decimal.Decimal(0), Variable('x', Quantity))
        self.assert_quantity(
            cast(Quantity, QuantityTemplate(0, None, 0, None)),
            decimal.Decimal(0), None, decimal.Decimal(0), None)
        self.assertRaises(TypeError, QuantityTemplate, x, x)
        self.assertRaises(TypeError, Quantity, 0, x, x)
        self.assertRaises(
            TypeError, QuantityTemplate, 0, x, None, x)
        self.assert_quantity_template(
            QuantityTemplate(x, None, x),
            QuantityVariable('x'), None, QuantityVariable('x'), None)
        self.assert_quantity_template(
            QuantityTemplate(x, None, x, Variable('x', DeepDataValue)),
            QuantityVariable('x'), None,
            QuantityVariable('x'), QuantityVariable('x'))
        self.assert_quantity_template(
            QuantityTemplate(
                x, None, Variable('x', DataValue),
                Variable('x', DeepDataValue)),
            QuantityVariable('x'), None,
            QuantityVariable('x'), QuantityVariable('x'))

    def test_instantiate(self) -> None:
        assert_type(
            QuantityTemplate(Variable('x')).instantiate({}), Term)
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
