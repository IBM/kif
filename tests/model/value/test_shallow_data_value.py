# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    Quantity,
    ShallowDataValue,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
    String,
    Text,
    Time,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_ShallowDataValueTestCase


class Test(kif_ShallowDataValueTestCase):

    def test_template_class(self) -> None:
        assert_type(
            ShallowDataValue.template_class, type[ShallowDataValueTemplate])
        self.assertIs(
            ShallowDataValue.template_class,
            ShallowDataValueTemplate)

    def test_variable_class(self) -> None:
        assert_type(
            ShallowDataValue.variable_class, type[ShallowDataValueVariable])
        self.assertIs(
            ShallowDataValue.variable_class, ShallowDataValueVariable)

    def test_check(self) -> None:
        assert_type(ShallowDataValue.check('x'), ShallowDataValue)
        super()._test_check(
            ShallowDataValue,
            success=[
                ('x', String('x')),
                (ExternalId('x'), ExternalId('x')),
                (IRI('x'), IRI('x')),
                (String('x'), String('x')),
                (Text('x', 'y'), Text('x', 'y')),
            ],
            failure=[
                (0, Quantity(0)),
                (1.0, Quantity(1.0)),
                (datetime.datetime(2024, 6, 26,
                                   tzinfo=datetime.timezone.utc),
                 Time(datetime.datetime(2024, 6, 26,
                                        tzinfo=datetime.timezone.utc))),
                (decimal.Decimal('.5'), Quantity('.5')),
                (Quantity(0, Item('x')), Quantity(0, Item('x'))),
                (Time('2024-06-27'), Time('2024-06-27')),
                Item('x'),
                Item(Variable('x')),
                Variable('x'),
                {},
            ])

    def test__init__(self):
        self.assert_abstract_class(ShallowDataValue)


if __name__ == '__main__':
    Test.main()
