# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    DataValueTemplate,
    DataValueVariable,
    Item,
    Quantity,
    String,
    Time,
)
from kif_lib.model import Datetime, Decimal, UTC
from kif_lib.typing import assert_type

from ...tests import kif_DataValueTestCase


class Test(kif_DataValueTestCase):

    def test_template_class(self) -> None:
        assert_type(DataValue.template_class, type[DataValueTemplate])

    def test_variable_class(self) -> None:
        assert_type(DataValue.variable_class, type[DataValueVariable])

    def test_check(self) -> None:
        self.assert_raises_check_error(
            DataValue, {}, DataValue.check)
        self.assert_raises_check_error(
            DataValue, Item('x'), DataValue.check)
        # success
        assert_type(DataValue.check(0), DataValue)
        self.assertEqual(DataValue.check('abc'), String('abc'))
        self.assertEqual(DataValue.check(Decimal(0)), Quantity(0))
        self.assertEqual(DataValue.check(
            Datetime(2024, 6, 26, tzinfo=UTC)), Time('2024-06-26'))

    def test__init__(self):
        self.assert_abstract_class(DataValue)


if __name__ == '__main__':
    Test.main()
