# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif import IRI, KIF_Object, NoValueSnak, Property, SnakSet

from .tests import kif_TestCase, main


class TestModelSnakSet(kif_TestCase):

    def test__preprocess_arg_snak_set(self):
        sset = SnakSet(NoValueSnak(Property('p')), Property('q')(IRI('x')))
        self.assertIs(
            sset, KIF_Object._preprocess_arg_snak_set(sset, 1))
        self.assertEqual(
            sset, KIF_Object._preprocess_arg_snak_set(list(sset), 1))

    def test__preprocess_optional_arg_snak_set(self):
        sset = SnakSet(NoValueSnak(Property('p')))
        self.assertIs(
            sset,
            KIF_Object._preprocess_optional_arg_snak_set(sset, 1, None))
        self.assertIs(
            sset,
            KIF_Object._preprocess_optional_arg_snak_set(None, 1, sset))
        self.assertIsNone(
            KIF_Object._preprocess_optional_arg_snak_set(None, 1, None))
        self.assertEqual(
            sset,
            KIF_Object._preprocess_optional_arg_snak_set(list(sset), 1))

    def test__init__(self):
        self.assertRaises(TypeError, SnakSet, 0)
        self.assertRaises(TypeError, SnakSet, Property('p'))
        self.assertFalse(bool(SnakSet()))
        self.assertTrue(bool(SnakSet(NoValueSnak(Property('p')))))
        self.assert_snak_set(SnakSet())
        snaks = [
            NoValueSnak(Property('p')),
            Property('p')(IRI('x')),
        ]
        self.assert_snak_set(SnakSet(*snaks), *snaks)

    def test__contains__(self):
        self.assertNotIn(0, SnakSet())
        self.assertIn(
            NoValueSnak(Property('p')), SnakSet(NoValueSnak(Property('p'))))
        self.assertNotIn(
            NoValueSnak(Property('p')), SnakSet(NoValueSnak(Property('q'))))

    def test_union(self):
        s1 = SnakSet(
            Property('p')(IRI('x')),
            Property('q')(IRI('y')))
        s2 = SnakSet(NoValueSnak(Property('p')))
        s3 = SnakSet()
        s4 = SnakSet(
            Property('q')(IRI('y')),
            Property('q')(IRI('z')))
        self.assertEqual(
            s1.union(s2, s3, s4),
            SnakSet(
                NoValueSnak(Property('p')),
                Property('p')(IRI('x')),
                Property('q')(IRI('y')),
                Property('q')(IRI('z'))))


if __name__ == '__main__':
    main()
