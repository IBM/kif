# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Snak

from .tests import kif_TestCase, main


class TestModelSnak(kif_TestCase):

    def test__preprocess_arg_plain_descriptor_field_field_mask(self):
        self.assertRaises(
            TypeError, Snak._preprocess_arg_snak_mask, 'abc', 1)
        self.assertEqual(
            Snak.VALUE_SNAK,
            Snak._preprocess_arg_snak_mask(Snak.VALUE_SNAK, 1))
        self.assertEqual(
            Snak.Mask(0),
            Snak._preprocess_arg_snak_mask(0, 1))

    def test__check_optional_arg_snak_mask(self):
        self.assertRaises(
            TypeError,
            Snak._check_optional_arg_snak_mask, 'abc')
        self.assertIsNone(Snak._check_optional_arg_snak_mask(None))
        self.assertEqual(
            Snak.VALUE_SNAK,
            Snak._check_optional_arg_snak_mask(None, Snak.VALUE_SNAK))
        self.assertEqual(
            Snak.Mask(0),
            Snak._check_optional_arg_snak_mask(Snak.Mask(0), Snak.VALUE_SNAK))

    def test__preprocess_optional_arg_plain_snak_mask(self):
        self.assertRaises(
            TypeError,
            Snak._preprocess_optional_arg_snak_mask, 'abc', 1)
        self.assertIsNone(
            Snak._preprocess_optional_arg_snak_mask(None, 1))
        self.assertEqual(
            Snak.VALUE_SNAK | Snak.NO_VALUE_SNAK,
            Snak._preprocess_optional_arg_snak_mask(
                None, 1, Snak.NO_VALUE_SNAK | Snak.VALUE_SNAK))
        self.assertEqual(
            Snak.VALUE_SNAK,
            Snak._preprocess_optional_arg_snak_mask(Snak.VALUE_SNAK, 1, None))
        self.assertEqual(
            Snak.Mask(0),
            Snak._preprocess_optional_arg_snak_mask(0, 1))


if __name__ == '__main__':
    main()
