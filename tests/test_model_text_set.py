# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif import KIF_Object, Property, Text, TextSet

from .tests import kif_TestCase, main


class TestModelTextSet(kif_TestCase):

    def test__preprocess_arg_text_set(self):
        tset = TextSet(Text('a'), Text('b'))
        self.assertIs(
            tset, KIF_Object._preprocess_arg_text_set(tset, 1))
        self.assertEqual(
            tset, KIF_Object._preprocess_arg_text_set(list(tset), 1))

    def test__preprocess_optional_arg_text_set(self):
        tset = TextSet(Text('p', 'pt'))
        self.assertIs(
            tset,
            KIF_Object._preprocess_optional_arg_text_set(tset, 1, None))
        self.assertIs(
            tset,
            KIF_Object._preprocess_optional_arg_text_set(None, 1, tset))
        self.assertIsNone(
            KIF_Object._preprocess_optional_arg_text_set(None, 1, None))
        self.assertEqual(
            tset,
            KIF_Object._preprocess_optional_arg_text_set(list(tset), 1))

    def test__init__(self):
        self.assertRaises(TypeError, TextSet, 0)
        self.assertRaises(TypeError, TextSet, Property('p'))
        self.assertFalse(bool(TextSet()))
        self.assertTrue(bool(TextSet(Text('p'))))
        self.assert_text_set(TextSet())
        texts = [
            Text('p'),
            Text('q')
        ]
        self.assert_text_set(TextSet(*texts), *texts)

    def test__contains__(self):
        self.assertNotIn(0, TextSet())
        self.assertIn(Text('p'), TextSet(Text('p')))
        self.assertNotIn(Text('p', 'pt'), TextSet(Text('p')))

    def test_union(self):
        s1 = TextSet(Text('p'), Text('q'))
        s2 = TextSet(Text('p'))
        s3 = TextSet()
        s4 = TextSet(Text('r'), Text('s'))
        self.assertEqual(
            s1.union(s2, s3, s4),
            TextSet(Text('p'), Text('q'), Text('r'), Text('s')))


if __name__ == '__main__':
    main()
