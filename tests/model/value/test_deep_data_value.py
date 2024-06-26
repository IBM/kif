# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DeepDataValue,
    DeepDataValueTemplate,
    DeepDataValueVariable,
    Item,
    Quantity,
    String,
    Time,
)
from kif_lib.model import Datetime, Decimal, UTC
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
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', DeepDataValue.check, 'x')
        self.assert_raises_check_error(
            DeepDataValue, {}, DeepDataValue.check)
        self.assert_raises_check_error(
            DeepDataValue, String('x'), DeepDataValue.check)
        self.assert_raises_check_error(
            DeepDataValue, Item('x'), DeepDataValue.check)
        # success
        assert_type(DeepDataValue.check(0), DeepDataValue)
        self.assertEqual(DeepDataValue.check(Decimal(0)), Quantity(0))
        self.assertEqual(DeepDataValue.check(
            Datetime(2024, 6, 26, tzinfo=UTC)), Time('2024-06-26'))

    def test__init__(self):
        self.assert_abstract_class(DeepDataValue)


if __name__ == '__main__':
    Test.main()
