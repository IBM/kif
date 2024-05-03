# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Item, KIF_Object
from kif_lib.model import ItemVariable, PropertyVariable, Variable

from ..tests import kif_TestCase


class Test(kif_TestCase):

    def test__check_arg_variable_class(self):
        self.assertRaises(
            TypeError, Variable._check_arg_variable_class, 0)
        self.assertRaises(
            TypeError, Variable._check_arg_variable_class, int)
        self.assertRaises(
            ValueError, Variable._check_arg_variable_class, KIF_Object)
        self.assertIs(
            Variable._check_arg_variable_class(Variable), Variable)
        self.assertIs(
            Variable._check_arg_variable_class(ItemVariable), ItemVariable)
        self.assertIs(
            Variable._check_arg_variable_class(Item), ItemVariable)

    def test__check_optional_arg_variable_class(self):
        self.assertRaises(
            TypeError, Variable._check_optional_arg_variable_class, 0)
        self.assertIsNone(
            Variable._check_optional_arg_variable_class(None))
        self.assertIs(
            Variable._check_optional_arg_variable_class(None, Variable),
            Variable)
        self.assertIs(
            Variable._check_optional_arg_variable_class(
                Item, PropertyVariable), ItemVariable)

    def test__preprocess_arg_variable_class(self):
        self.assertRaises(
            TypeError, Variable._preprocess_arg_variable_class, 0, 1)
        self.assertRaises(
            TypeError, Variable._preprocess_arg_variable_class, int, 1)
        self.assertIs(
            Variable._preprocess_arg_variable_class(ItemVariable, 1),
            ItemVariable)
        self.assertIs(
            Variable._preprocess_arg_variable_class(Item, 1),
            ItemVariable)

    def test__preprocess_optional_arg_variable_class(self):
        self.assertRaises(
            TypeError,
            Variable._preprocess_optional_arg_variable_class, 0, 1)
        self.assertRaises(
            TypeError,
            Variable._preprocess_optional_arg_variable_class, int, 1)
        self.assertIsNone(
            Variable._preprocess_optional_arg_variable_class(None, 1))
        self.assertEqual(
            Variable._preprocess_optional_arg_variable_class(
                None, 1, ItemVariable), ItemVariable)
        self.assertEqual(
            Variable._preprocess_optional_arg_variable_class(
                Item, 1, PropertyVariable), ItemVariable)


if __name__ == '__main__':
    Test.main()
