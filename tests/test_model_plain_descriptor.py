# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import PlainDescriptor

from .tests import kif_TestCase, main


class TestModelPlainDescriptor(kif_TestCase):

    def test__preprocess_arg_plain_descriptor_field_field_mask(self):
        self.assertRaises(
            TypeError,
            PlainDescriptor._preprocess_arg_plain_descriptor_field_mask,
            'abc', 1)
        self.assertEqual(
            PlainDescriptor.LABEL,
            PlainDescriptor._preprocess_arg_plain_descriptor_field_mask(
                PlainDescriptor.LABEL, 1))
        self.assertEqual(
            PlainDescriptor.FieldMask(0),
            PlainDescriptor._preprocess_arg_plain_descriptor_field_mask(0, 1))

    def test__preprocess_optional_arg_plain_descriptor_field_mask(self):
        self.assertRaises(
            TypeError,
            PlainDescriptor.
            _preprocess_optional_arg_plain_descriptor_field_mask,
            'abc', 1)
        self.assertIsNone(
            PlainDescriptor.
            _preprocess_optional_arg_plain_descriptor_field_mask(
                None, 1))
        self.assertEqual(
            PlainDescriptor.LABEL,
            PlainDescriptor.
            _preprocess_optional_arg_plain_descriptor_field_mask(
                None, 1, PlainDescriptor.LABEL))
        self.assertEqual(
            PlainDescriptor.LABEL,
            PlainDescriptor.
            _preprocess_optional_arg_plain_descriptor_field_mask(
                PlainDescriptor.LABEL, 1, None))
        self.assertEqual(
            PlainDescriptor.FieldMask(0),
            PlainDescriptor.
            _preprocess_optional_arg_plain_descriptor_field_mask(
                0, 1))


if __name__ == '__main__':
    main()
