# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import decimal

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    Property,
    Quantity,
    QuantityDatatype,
    QuantityTemplate,
    QuantityVariable,
    String,
    Text,
)
from kif_lib.typing import assert_type

from ...tests import kif_DeepDataValueTestCase


class Test(kif_DeepDataValueTestCase):

    def test_datatype_class(self) -> None:
        assert_type(Quantity.datatype_class, type[QuantityDatatype])
        self.assertIs(Quantity.datatype_class, QuantityDatatype)

    def test_datatype(self) -> None:
        assert_type(Quantity.datatype, QuantityDatatype)
        self.assert_quantity_datatype(Quantity.datatype)

    def test_template_class(self) -> None:
        assert_type(Quantity.template_class, type[QuantityTemplate])
        self.assertIs(Quantity.template_class, QuantityTemplate)

    def test_variable_class(self) -> None:
        assert_type(Quantity.variable_class, type[QuantityVariable])
        self.assertIs(Quantity.variable_class, QuantityVariable)

    def test_check(self) -> None:
        assert_type(Quantity.check(0), Quantity)
        self._test_check(
            Quantity,
            success=[
                (decimal.Decimal(0), Quantity(decimal.Decimal(0))),
                (0, Quantity(0)),
                (0.1, Quantity(0.1)),
                ('0.1', Quantity('0.1')),
                (String('0'), Quantity(0)),
                (Quantity('0'), Quantity(0)),
            ],
            failure=[
                IRI('x'),
                Item('x'),
                Text('x'),
            ],
            failure_value_error=[
                'x',
                ExternalId('x'),
                String('x'),
            ])

    def test__init__(self) -> None:
        assert_type(Quantity(0), Quantity)
        self._test__init__(
            Quantity,
            self.assert_quantity,
            success=[
                ((0,), Quantity(0)),
                ((0, 'x'), Quantity(0, Item('x'))),
                ((0, Item('x')), Quantity(0, Item('x'))),
                ((0, None, 1), Quantity(0, None, 1)),
                ((0, None, None, 2), Quantity(0, None, None, 2)),
                (('0', 'x', None, 2), Quantity(0, Item('x'), None, 2)),
                ((0.1, 'x', decimal.Decimal(8), 2),
                 Quantity(0.1, Item('x'), decimal.Decimal(8), 2)),
            ],
            failure=[
                ({},),
                (0, Property('x')),
                (0, None, Property('x')),
                (0, None, None, Property('x')),
            ])

    def test_get_unit(self):
        self.assertEqual(Quantity(0, Item('x')).get_unit(), Item('x'))
        self.assertEqual(Quantity(0).get_unit(Item('x')), Item('x'))
        self.assertEqual(Quantity(0).get_unit(Item(IRI('x'))), Item('x'))
        self.assertIsNone(Quantity(0).get_unit())

    def test_get_lower_bound(self):
        self.assertEqual(
            Quantity(0, None, 1).get_lower_bound(), decimal.Decimal('1'))
        self.assertEqual(
            Quantity(0, None).get_lower_bound(
                decimal.Decimal('1.')), decimal.Decimal('1.'))
        self.assertIsNone(Quantity(0, None).get_lower_bound())

    def test_get_upper_bound(self):
        self.assertEqual(
            Quantity(0, None, 1, 2).get_upper_bound(),
            decimal.Decimal('2'))
        self.assertEqual(
            Quantity(0).get_upper_bound(decimal.Decimal(2)),
            decimal.Decimal(2))
        self.assertIsNone(Quantity(0, None).get_upper_bound())


if __name__ == '__main__':
    Test.main()
