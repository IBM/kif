# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    Item,
    Property,
    Quantity,
    QuantityDatatype,
    QuantityTemplate,
    QuantityVariable,
    String,
    StringDatatype,
    Text,
    TextTemplate,
    Variable,
)
from kif_lib.model import Decimal
from kif_lib.typing import assert_type

from ...tests import kif_DeepDataValueTestCase


class Test(kif_DeepDataValueTestCase):

    def test_datatype_class(self) -> None:
        assert_type(Quantity.datatype_class, type[QuantityDatatype])

    def test_datatype(self) -> None:
        assert_type(Quantity.datatype, QuantityDatatype)
        self.assertIsInstance(String.datatype, StringDatatype)

    def test_template_class(self) -> None:
        assert_type(Quantity.template_class, type[QuantityTemplate])

    def test_variable_class(self) -> None:
        assert_type(Quantity.variable_class, type[QuantityVariable])

    def test_check(self) -> None:
        assert_type(Quantity.check(0), Quantity)
        self.assert_raises_check_error(
            Quantity, 'abc', Quantity, None, 1, ValueError)
        self._test_check(
            Quantity,
            success=[
                (Decimal(0), Quantity(Decimal(0))),
                (0, Quantity(0)),
                (0.1, Quantity(0.1)),
                ('0.1', Quantity('0.1')),
                (String('0'), Quantity(0)),
            ],
            failure=[
                IRI('x'),
                Item('x'),
                Text('x'),
                TextTemplate(Variable('x')),
                Variable('x', Item),
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
                ((0.1, 'x', Decimal(8), 2),
                 Quantity(0.1, Item('x'), Decimal(8), 2)),
            ],
            failure=[
                ({},),
                (0, Property('x')),
                (0, None, Property('x')),
                (0, None, None, Property('x')),
            ])


if __name__ == '__main__':
    Test.main()
