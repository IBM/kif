# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Fingerprint, IRI, Item, NoValueSnak, Property, SnakSet

from .tests import kif_TestCase


class TestModelFingerprintFingerprint(kif_TestCase):

    def test__preprocess_arg_fingerprint(self):
        self.assertEqual(
            Fingerprint._preprocess_arg_fingerprint(IRI('x'), 1),
            Fingerprint(IRI('x')))
        self.assertEqual(
            Fingerprint._preprocess_arg_fingerprint(
                SnakSet(NoValueSnak(Property('p'))), 1),
            Fingerprint(SnakSet(NoValueSnak(Property('p')))))
        self.assertEqual(
            Fingerprint._preprocess_arg_fingerprint(
                [NoValueSnak(Property('p'))], 1),
            Fingerprint([NoValueSnak(Property('p'))]))

    def test__preprocess_optional_arg_fingerprint(self):
        self.assertEqual(
            Fingerprint._preprocess_optional_arg_fingerprint(IRI('x'), 1),
            Fingerprint(IRI('x')))
        self.assertEqual(
            Fingerprint._preprocess_optional_arg_fingerprint(
                None, 1, Fingerprint(IRI('x'))),
            Fingerprint(IRI('x')))
        self.assertEqual(
            Fingerprint._preprocess_optional_arg_fingerprint(None, 1, None),
            None)

    def test__init__(self):
        # self.assertRaises(TypeError, Fingerprint, 0)
        self.assert_fingerprint(Fingerprint(IRI('x')), IRI('x'))
        self.assert_fingerprint(Fingerprint(Fingerprint(IRI('x'))), IRI('x'))
        self.assert_fingerprint(Fingerprint(Item('x')), Item('x'))
        self.assert_fingerprint(Fingerprint(SnakSet()), SnakSet())
        self.assert_fingerprint(
            Fingerprint([Property('x')(Item('y'))]),
            SnakSet(Property('x')(Item('y'))))
        self.assert_fingerprint(
            Fingerprint(Property('x')(Item('y'))),
            SnakSet(Property('x')(Item('y'))))

    def test_get_value(self):
        fp = Fingerprint(IRI('x'))
        self.assertEqual(fp.value, IRI('x'))
        self.assertEqual(fp.get_value(), IRI('x'))
        self.assertIsNone(fp.snak_set)
        self.assertIsNone(fp.get_snak_set())
        self.assertEqual(fp.get_snak_set(SnakSet()), SnakSet())

    def test_get_snak_set(self):
        fp = Fingerprint(Property('x')(Item('y')))
        self.assertEqual(fp.snak_set, SnakSet(Property('x')(Item('y'))))
        self.assertEqual(fp.get_snak_set(), SnakSet(Property('x')(Item('y'))))
        self.assertIsNone(fp.value)
        self.assertIsNone(fp.get_value())
        self.assertEqual(fp.get_value(IRI('x')), IRI('x'))


if __name__ == '__main__':
    TestModelFingerprintFingerprint.main()
