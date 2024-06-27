# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal

from kif_lib import (
    Item,
    Quantity,
    String,
    Time,
    Value,
    ValueTemplate,
    ValueVariable,
)
from kif_lib.typing import assert_type

from ...tests import kif_ValueTestCase


class Test(kif_ValueTestCase):

    def test_template_class(self) -> None:
        assert_type(Value.template_class, type[ValueTemplate])

    def test_variable_class(self) -> None:
        assert_type(Value.variable_class, type[ValueVariable])

    def test_check(self) -> None:
        self.assert_raises_check_error(Value, {}, Value.check)
        # success
        assert_type(Value.check(0), Value)
        self.assertEqual(Value.check('abc'), String('abc'))
        self.assertEqual(
            Value.check(datetime.datetime(
                2024, 6, 26, tzinfo=datetime.timezone.utc)),
            Time('2024-06-26'))
        self.assertEqual(Value.check(decimal.Decimal(0)), Quantity(0))
        self.assertEqual(Value.check(Item('x')), Item('x'))

    def test__init__(self):
        self.assert_abstract_class(Value)


if __name__ == '__main__':
    Test.main()
