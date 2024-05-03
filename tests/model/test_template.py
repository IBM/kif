# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Item, KIF_Object
from kif_lib.model import ItemTemplate, PropertyTemplate, Template

from ..tests import kif_TestCase


class Test(kif_TestCase):

    def test__check_arg_template_class(self):
        self.assertRaises(
            TypeError, Template._check_arg_template_class, 0)
        self.assertRaises(
            TypeError, Template._check_arg_template_class, int)
        self.assertRaises(
            ValueError, Template._check_arg_template_class, KIF_Object)
        self.assertIs(
            Template._check_arg_template_class(Template), Template)
        self.assertIs(
            Template._check_arg_template_class(ItemTemplate), ItemTemplate)
        self.assertIs(
            Template._check_arg_template_class(Item), ItemTemplate)

    def test__check_optional_arg_template_class(self):
        self.assertRaises(
            TypeError, Template._check_optional_arg_template_class, 0)
        self.assertIsNone(
            Template._check_optional_arg_template_class(None))
        self.assertIs(
            Template._check_optional_arg_template_class(None, Template),
            Template)
        self.assertIs(
            Template._check_optional_arg_template_class(
                Item, PropertyTemplate), ItemTemplate)

    def test__preprocess_arg_template_class(self):
        self.assertRaises(
            TypeError, Template._preprocess_arg_template_class, 0, 1)
        self.assertRaises(
            TypeError, Template._preprocess_arg_template_class, int, 1)
        self.assertIs(
            Template._preprocess_arg_template_class(ItemTemplate, 1),
            ItemTemplate)
        self.assertIs(
            Template._preprocess_arg_template_class(Item, 1),
            ItemTemplate)

    def test__preprocess_optional_arg_template_class(self):
        self.assertRaises(
            TypeError,
            Template._preprocess_optional_arg_template_class, 0, 1)
        self.assertRaises(
            TypeError,
            Template._preprocess_optional_arg_template_class, int, 1)
        self.assertIsNone(
            Template._preprocess_optional_arg_template_class(None, 1))
        self.assertEqual(
            Template._preprocess_optional_arg_template_class(
                None, 1, ItemTemplate), ItemTemplate)
        self.assertEqual(
            Template._preprocess_optional_arg_template_class(
                Item, 1, PropertyTemplate), ItemTemplate)


if __name__ == '__main__':
    Test.main()
