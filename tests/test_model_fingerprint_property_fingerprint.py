# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    Item,
    NoValueSnak,
    Property,
    PropertyFingerprint,
    SnakSet,
)

from .tests import kif_TestCase


class TestModelFingerprintPropertyFingerprint(kif_TestCase):

    def test_check(self):
        self.assertEqual(
            PropertyFingerprint.check(Property('x')),
            PropertyFingerprint(Property('x')))
        self.assertEqual(
            PropertyFingerprint.check(
                SnakSet(NoValueSnak(Property('p')))),
            PropertyFingerprint(SnakSet(NoValueSnak(Property('p')))))
        self.assertEqual(
            PropertyFingerprint.check(
                [NoValueSnak(Property('p'))]),
            PropertyFingerprint([NoValueSnak(Property('p'))]))
        self.assertEqual(
            PropertyFingerprint.check(Property('x')),
            PropertyFingerprint(Property('x')))
        self.assertEqual(
            PropertyFingerprint.check_optional(
                None, PropertyFingerprint(Property('x'))),
            PropertyFingerprint(Property('x')))
        self.assertEqual(PropertyFingerprint.check_optional(None), None)

    def test__init__(self):
        self.assertRaises(TypeError, PropertyFingerprint, 0)
        self.assertRaises(TypeError, PropertyFingerprint, Item('x'))
        self.assert_property_fingerprint(
            PropertyFingerprint(IRI('x')), Property('x'))
        self.assert_property_fingerprint(
            PropertyFingerprint(Property('x')), Property('x'))
        self.assert_property_fingerprint(
            PropertyFingerprint(
                PropertyFingerprint(Property('x'))), Property('x'))
        self.assert_property_fingerprint(
            PropertyFingerprint(SnakSet()), SnakSet())
        self.assert_property_fingerprint(
            PropertyFingerprint([Property('x')(Item('y'))]),
            SnakSet(Property('x')(Item('y'))))
        self.assert_property_fingerprint(
            PropertyFingerprint(Property('x')(Item('y'))),
            SnakSet(Property('x')(Item('y'))))

    def test_get_property(self):
        fp = PropertyFingerprint(Property('x'))
        self.assertEqual(fp.property, Property('x'))
        self.assertEqual(fp.get_property(), Property('x'))
        self.assertIsNone(fp.snak_set)
        self.assertIsNone(fp.get_snak_set())
        self.assertEqual(fp.get_snak_set(SnakSet()), SnakSet())
        fp = PropertyFingerprint(SnakSet())
        self.assertIsNone(fp.property)
        self.assertIsNone(fp.get_property())
        self.assertEqual(fp.get_property(Property('x')), Property('x'))


if __name__ == '__main__':
    TestModelFingerprintPropertyFingerprint.main()
