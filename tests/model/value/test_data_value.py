# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal

from kif_lib import (
    DataValue,
    DataValueTemplate,
    DataValueVariable,
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

from ...tests import kif_DataValueTestCase


class Test(kif_DataValueTestCase):

    def test_template_class(self) -> None:
        assert_type(DataValue.template_class, type[DataValueTemplate])
        self.assertIs(DataValue.template_class, DataValueTemplate)

    def test_variable_class(self) -> None:
        assert_type(DataValue.variable_class, type[DataValueVariable])
        self.assertIs(DataValue.variable_class, DataValueVariable)

    def test_check(self) -> None:
        assert_type(DataValue.check(0), DataValue)
        super()._test_check(
            DataValue,
            success=[
                ('x', String('x')),
                (0, Quantity(0)),
                (1.0, Quantity(1.0)),
                (datetime.datetime(2024, 6, 26,
                                   tzinfo=datetime.timezone.utc),
                 Time(datetime.datetime(2024, 6, 26,
                                        tzinfo=datetime.timezone.utc))),
                (decimal.Decimal('.5'), Quantity('.5')),
                (ExternalId('x'), ExternalId('x')),
                (IRI('x'), IRI('x')),
                (Quantity(0, Item('x')), Quantity(0, Item('x'))),
                (String('x'), String('x')),
                (Text('x', 'y'), Text('x', 'y')),
                (Time('2024-06-27'), Time('2024-06-27')),
            ],
            failure=[
                Item('x'),
                Item(Variable('x')),
                Variable('x'),
                {},
            ])

    def test__init__(self):
        self.assert_abstract_class(DataValue)


if __name__ == '__main__':
    Test.main()
