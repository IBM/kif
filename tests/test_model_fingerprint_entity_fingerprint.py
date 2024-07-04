# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    EntityFingerprint,
    IRI,
    Item,
    NoValueSnak,
    Property,
    SnakSet,
)

from .tests import kif_TestCase


class TestModelFingerprintEntityFingerprint(kif_TestCase):

    def test_check(self):
        self.assertEqual(
            EntityFingerprint.check(Item('x')),
            EntityFingerprint(Item('x')))
        self.assertEqual(
            EntityFingerprint.check(
                SnakSet(NoValueSnak(Property('p')))),
            EntityFingerprint(SnakSet(NoValueSnak(Property('p')))))
        self.assertEqual(
            EntityFingerprint.check(
                [NoValueSnak(Property('p'))]),
            EntityFingerprint([NoValueSnak(Property('p'))]))
        self.assertEqual(
            EntityFingerprint.check_optional(
                Item('x')),
            EntityFingerprint(Item('x')))
        self.assertEqual(
            EntityFingerprint.check_optional(
                None, EntityFingerprint(Item('x'))),
            EntityFingerprint(Item('x')))
        self.assertEqual(
            EntityFingerprint.check_optional(None), None)

    def test__init__(self):
        self.assertRaises(TypeError, EntityFingerprint, 0)
        self.assertRaises(TypeError, EntityFingerprint, IRI('x'))
        self.assert_entity_fingerprint(
            EntityFingerprint(Item('x')), Item('x'))
        self.assert_entity_fingerprint(
            EntityFingerprint(EntityFingerprint(Item('x'))), Item('x'))
        self.assert_entity_fingerprint(
            EntityFingerprint(SnakSet()), SnakSet())
        self.assert_entity_fingerprint(
            EntityFingerprint(Property('x')(Item('y'))),
            SnakSet(Property('x')(Item('y'))))
        self.assert_entity_fingerprint(
            EntityFingerprint([Property('x')(Item('y'))]),
            SnakSet(Property('x')(Item('y'))))

    def test_get_entity(self):
        fp = EntityFingerprint(Item('x'))
        self.assertEqual(fp.entity, Item('x'))
        self.assertEqual(fp.get_entity(), Item('x'))
        self.assertIsNone(fp.snak_set)
        self.assertIsNone(fp.get_snak_set())
        self.assertEqual(fp.get_snak_set(SnakSet()), SnakSet())
        fp = EntityFingerprint(SnakSet())
        self.assertIsNone(fp.entity)
        self.assertIsNone(fp.get_entity())
        self.assertEqual(fp.get_entity(Property('x')), Property('x'))


if __name__ == '__main__':
    TestModelFingerprintEntityFingerprint.main()
