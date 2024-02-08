# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import PlainDescriptor

from .tests import kif_TestCase, main


class TestModelPlainDescriptor(kif_TestCase):

    def test__preprocess_arg_plain_descriptor_attribute_mask(self):
        self.assertRaises(
            TypeError,
            PlainDescriptor._preprocess_arg_plain_descriptor_attribute_mask,
            'abc', 1)
        self.assertEqual(
            PlainDescriptor.LABEL,
            PlainDescriptor._preprocess_arg_plain_descriptor_attribute_mask(
                PlainDescriptor.LABEL, 1))
        self.assertEqual(
            PlainDescriptor.AttributeMask(0),
            PlainDescriptor.
            _preprocess_arg_plain_descriptor_attribute_mask(0, 1))

    def test__check_optional_arg_plain_descriptor_attribute_mask(self):
        self.assertRaises(
            TypeError,
            PlainDescriptor.
            _check_optional_arg_plain_descriptor_attribute_mask, 'abc')
        self.assertIsNone(
            PlainDescriptor.
            _check_optional_arg_plain_descriptor_attribute_mask(None))
        self.assertEqual(
            PlainDescriptor.LABEL | PlainDescriptor.ALIASES,
            PlainDescriptor.
            _check_optional_arg_plain_descriptor_attribute_mask(
                None, PlainDescriptor.ALIASES | PlainDescriptor.LABEL))
        self.assertEqual(
            PlainDescriptor.AttributeMask(0),
            PlainDescriptor.
            _check_optional_arg_plain_descriptor_attribute_mask(
                PlainDescriptor.AttributeMask(0), PlainDescriptor.LABEL))

    def test__preprocess_optional_arg_plain_descriptor_attribute_mask(self):
        self.assertRaises(
            TypeError,
            PlainDescriptor.
            _preprocess_optional_arg_plain_descriptor_attribute_mask,
            'abc', 1)
        self.assertIsNone(
            PlainDescriptor.
            _preprocess_optional_arg_plain_descriptor_attribute_mask(
                None, 1))
        self.assertEqual(
            PlainDescriptor.LABEL,
            PlainDescriptor.
            _preprocess_optional_arg_plain_descriptor_attribute_mask(
                None, 1, PlainDescriptor.LABEL))
        self.assertEqual(
            PlainDescriptor.LABEL,
            PlainDescriptor.
            _preprocess_optional_arg_plain_descriptor_attribute_mask(
                PlainDescriptor.LABEL, 1, None))
        self.assertEqual(
            PlainDescriptor.AttributeMask(0),
            PlainDescriptor.
            _preprocess_optional_arg_plain_descriptor_attribute_mask(
                0, 1))


if __name__ == '__main__':
    main()
