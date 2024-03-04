# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Descriptor

from .tests import kif_TestCase


class TestDescriptor(kif_TestCase):

    def test__preprocess_arg_descriptor_attribute_mask(self):
        self.assertRaises(
            TypeError,
            Descriptor._preprocess_arg_descriptor_attribute_mask,
            'abc', 1)
        self.assertEqual(
            Descriptor.LABEL,
            Descriptor._preprocess_arg_descriptor_attribute_mask(
                Descriptor.LABEL, 1))
        self.assertEqual(
            Descriptor.AttributeMask(0),
            Descriptor._preprocess_arg_descriptor_attribute_mask(0, 1))

    def test__check_optional_arg_descriptor_attribute_mask(self):
        self.assertRaises(
            TypeError,
            Descriptor._check_optional_arg_descriptor_attribute_mask, 'abc')
        self.assertIsNone(
            Descriptor._check_optional_arg_descriptor_attribute_mask(None))
        self.assertEqual(
            Descriptor.LABEL | Descriptor.LEMMA,
            Descriptor._check_optional_arg_descriptor_attribute_mask(
                None, Descriptor.LEMMA | Descriptor.LABEL))
        self.assertEqual(
            Descriptor.AttributeMask(0),
            Descriptor._check_optional_arg_descriptor_attribute_mask(
                Descriptor.AttributeMask(0), Descriptor.LABEL))

    def test__preprocess_optional_arg_descriptor_attribute_mask(self):
        self.assertRaises(
            TypeError,
            Descriptor._preprocess_optional_arg_descriptor_attribute_mask,
            'abc', 1)
        self.assertIsNone(
            Descriptor._preprocess_optional_arg_descriptor_attribute_mask(
                None, 1))
        self.assertEqual(
            Descriptor.LABEL,
            Descriptor._preprocess_optional_arg_descriptor_attribute_mask(
                None, 1, Descriptor.LABEL))
        self.assertEqual(
            Descriptor.LABEL,
            Descriptor._preprocess_optional_arg_descriptor_attribute_mask(
                Descriptor.LABEL, 1, None))
        self.assertEqual(
            Descriptor.AttributeMask(0),
            Descriptor._preprocess_optional_arg_descriptor_attribute_mask(
                0, 1))


if __name__ == '__main__':
    TestDescriptor.main()
