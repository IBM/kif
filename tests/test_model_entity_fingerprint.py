# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif import EntityFingerprint, IRI, Item, NoValueSnak, Property, SnakSet

from .tests import kif_TestCase, main


class TestModelEntityFingerprint(kif_TestCase):

    def test__preprocess_arg_entity_fingerprint(self):
        self.assertEqual(
            EntityFingerprint._preprocess_arg_entity_fingerprint(
                Item('x'), 1),
            EntityFingerprint(Item('x')))
        self.assertEqual(
            EntityFingerprint._preprocess_arg_entity_fingerprint(
                SnakSet(NoValueSnak(Property('p'))), 1),
            EntityFingerprint(SnakSet(NoValueSnak(Property('p')))))
        self.assertEqual(
            EntityFingerprint._preprocess_arg_entity_fingerprint(
                [NoValueSnak(Property('p'))], 1),
            EntityFingerprint([NoValueSnak(Property('p'))]))

    def test__preprocess_optional_arg_entity_fingerprint(self):
        self.assertEqual(
            EntityFingerprint._preprocess_optional_arg_entity_fingerprint(
                Item('x'), 1),
            EntityFingerprint(Item('x')))
        self.assertEqual(
            EntityFingerprint._preprocess_optional_arg_entity_fingerprint(
                None, 1, EntityFingerprint(Item('x'))),
            EntityFingerprint(Item('x')))
        self.assertEqual(
            EntityFingerprint._preprocess_optional_arg_entity_fingerprint(
                None, 1, None), None)

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
    main()
