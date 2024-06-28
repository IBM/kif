# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal

from kif_lib import (
    DeepDataValue,
    DeepDataValueTemplate,
    DeepDataValueVariable,
    ExternalId,
    IRI,
    Item,
    Quantity,
    String,
    Text,
    Time,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_DeepDataValueTestCase


class Test(kif_DeepDataValueTestCase):

    def test_template_class(self) -> None:
        assert_type(
            DeepDataValue.template_class, type[DeepDataValueTemplate])

    def test_variable_class(self) -> None:
        assert_type(
            DeepDataValue.variable_class, type[DeepDataValueVariable])

    def test_check(self) -> None:
        assert_type(DeepDataValue.check(0), DeepDataValue)
        super()._test_check(
            DeepDataValue,
            success=[
                (0, Quantity(0)),
                (1.0, Quantity(1.0)),
                (datetime.datetime(2024, 6, 26,
                                   tzinfo=datetime.timezone.utc),
                 Time(datetime.datetime(2024, 6, 26,
                                        tzinfo=datetime.timezone.utc))),
                (decimal.Decimal('.5'), Quantity('.5')),
                (Time('2024-06-27'), Time('2024-06-27')),
                (Quantity(0, Item('x')), Quantity(0, Item('x'))),
            ],
            failure=[
                ('x', String('x')),
                (ExternalId('x'), ExternalId('x')),
                (IRI('x'), IRI('x')),
                (String('x'), String('x')),
                (Text('x', 'y'), Text('x', 'y')),
                Item('x'),
                Item(Variable('x')),
                Variable('x'),
                {},
            ])

    def test__init__(self):
        self.assert_abstract_class(DeepDataValue)


if __name__ == '__main__':
    Test.main()
