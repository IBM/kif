# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Item, Quantity, String, Value

from .tests import kif_TestCase


class TestModelValueValue(kif_TestCase):

    def test__preprocess_arg_value(self):
        self.assertRaises(TypeError, Value._preprocess_arg_value, dict(), 1)
        self.assertEqual(Value._preprocess_arg_value(5, 1), Quantity(5))
        self.assertEqual(Value._preprocess_arg_value('abc', 1), String('abc'))
        self.assertEqual(Value._preprocess_arg_value(Item('x'), 1), Item('x'))


if __name__ == '__main__':
    TestModelValueValue.main()
