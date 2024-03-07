# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import KIF_Object, Property, Quantity, String, Text, ValueSet

from .tests import kif_TestCase


class TestModelValueSetValueSet(kif_TestCase):

    def test__preprocess_arg_value_set(self):
        vset = ValueSet(Text('a'), Property('b'))
        self.assertIs(
            vset, KIF_Object._preprocess_arg_value_set(vset, 1))
        self.assertEqual(
            vset, KIF_Object._preprocess_arg_value_set(list(vset), 1))

    def test__preprocess_optional_arg_value_set(self):
        vset = ValueSet(Text('p', 'pt'))
        self.assertIs(
            vset,
            KIF_Object._preprocess_optional_arg_value_set(vset, 1, None))
        self.assertIs(
            vset,
            KIF_Object._preprocess_optional_arg_value_set(None, 1, vset))
        self.assertIsNone(
            KIF_Object._preprocess_optional_arg_value_set(None, 1, None))
        self.assertEqual(
            vset,
            KIF_Object._preprocess_optional_arg_value_set(list(vset), 1))

    def test__init__(self):
        self.assertRaises(TypeError, ValueSet, dict())
        self.assertRaises(TypeError, ValueSet, Property('p')(Text('q')))
        self.assertFalse(bool(ValueSet()))
        self.assertTrue(bool(ValueSet(Property('p'))))
        self.assert_value_set(ValueSet())
        self.assert_value_set(
            ValueSet(Property('p'), Text('q'), 0, 'x'),
            Property('p'), Quantity(0), String('x'), Text('q'))

    def test__contains__(self):
        self.assertNotIn(0, ValueSet())
        self.assertIn(Text('p'), ValueSet(Text('p')))
        self.assertNotIn(Text('p', 'pt'), ValueSet(Text('p')))

    def test_union(self):
        s1 = ValueSet(Text('p'), Property('q'))
        s2 = ValueSet(Text('p'))
        s3 = ValueSet()
        s4 = ValueSet(Text('r'), Text('s'))
        self.assertEqual(
            s1.union(s2, s3, s4),
            ValueSet(Text('p'), Property('q'), Text('r'), Text('s')))


if __name__ == '__main__':
    TestModelValueSetValueSet.main()
