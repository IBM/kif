# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif import IRI, KIF_Object, KIF_ObjectSet, NoValueSnak, Property

from .tests import kif_TestCase, main


class TestModelKIF_ObjectSet(kif_TestCase):

    def test__preprocess_arg_kif_object_set(self):
        s = KIF_ObjectSet(Property('p'), Property('q')(IRI('x')))
        self.assertIs(s, KIF_Object._preprocess_arg_kif_object_set(s, 1))
        self.assertEqual(
            s, KIF_Object._preprocess_arg_kif_object_set(list(s), 1))

    def test__preprocess_optional_arg_snak_set(self):
        s = KIF_ObjectSet(KIF_ObjectSet(Property('p')))
        self.assertIs(
            s,
            KIF_Object._preprocess_optional_arg_kif_object_set(s, 1, None))
        self.assertIs(
            s,
            KIF_Object._preprocess_optional_arg_kif_object_set(None, 1, s))
        self.assertIsNone(
            KIF_Object._preprocess_optional_arg_kif_object_set(None, 1, None))
        self.assertEqual(
            s,
            KIF_Object._preprocess_optional_arg_kif_object_set(list(s), 1))

    def test__init__(self):
        self.assertRaises(TypeError, KIF_ObjectSet, 0)
        self.assertFalse(bool(KIF_ObjectSet()))
        self.assertTrue(bool(KIF_ObjectSet(Property('p'))))
        self.assert_kif_object_set(KIF_ObjectSet())
        objs = [
            IRI('x'),
            Property('p'),
            Property('p')(IRI('x')),
        ]
        self.assert_kif_object_set(KIF_ObjectSet(*objs), *objs)

    def test__contains__(self):
        self.assertNotIn(0, KIF_ObjectSet())
        self.assertIn(
            NoValueSnak(Property('p')),
            KIF_ObjectSet(NoValueSnak(Property('p'))))
        self.assertNotIn(
            NoValueSnak(Property('p')),
            KIF_ObjectSet(NoValueSnak(Property('q'))))

    def test__union(self):
        s1 = KIF_ObjectSet(
            Property('p')(IRI('x')),
            Property('q')(IRI('y')))
        s2 = KIF_ObjectSet(NoValueSnak(Property('p')))
        s3 = KIF_ObjectSet()
        s4 = KIF_ObjectSet(
            Property('q')(IRI('y')),
            Property('q')(IRI('z')))
        self.assertEqual(
            s1._union([s2, s3, s4]),
            KIF_ObjectSet(
                NoValueSnak(Property('p')),
                Property('p')(IRI('x')),
                Property('q')(IRI('y')),
                Property('q')(IRI('z'))))


if __name__ == '__main__':
    main()
