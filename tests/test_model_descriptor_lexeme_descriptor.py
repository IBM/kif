# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import LexemeDescriptor, Text
from kif_lib.vocabulary import wd

from .tests import kif_TestCase


class TestModelDescriptorLexemeDescriptor(kif_TestCase):

    def test__init__(self):
        # bad arguments
        self.assertRaises(TypeError, LexemeDescriptor, 0)
        self.assertRaises(TypeError, LexemeDescriptor, 0, None)
        self.assertRaises(TypeError, LexemeDescriptor, 'x', wd.English, 0)
        self.assertRaises(TypeError, LexemeDescriptor, None, wd.English, 0)
        self.assertRaises(TypeError, LexemeDescriptor, 'x', 0, wd.verb)
        self.assertRaises(TypeError, LexemeDescriptor, 'x', wd.verb, wd.mass)
        # good arguments
        self.assert_lexeme_descriptor(LexemeDescriptor(), None, None, None)
        self.assert_lexeme_descriptor(
            LexemeDescriptor('x', wd.verb, wd.English),
            Text('x'), wd.verb, wd.English)

    def test_get_lemma(self):
        self.assertEqual(LexemeDescriptor('x').get_lemma(), Text('x'))
        self.assertEqual(LexemeDescriptor(
            Text('x', 'es')).lemma, Text('x', 'es'))
        self.assertEqual(
            LexemeDescriptor().get_lemma(Text('x', 'es')), Text('x', 'es'))
        self.assertIsNone(LexemeDescriptor().get_lemma())

    def test_get_category(self):
        self.assertEqual(
            LexemeDescriptor(None, wd.verb).get_category(), wd.verb)
        self.assertEqual(LexemeDescriptor(None, wd.verb).category, wd.verb)
        self.assertEqual(LexemeDescriptor().get_category(wd.verb), wd.verb)
        self.assertIsNone(LexemeDescriptor().get_category())

    def test_get_language(self):
        self.assertEqual(
            LexemeDescriptor(None, None, wd.English).get_language(),
            wd.English)
        self.assertEqual(
            LexemeDescriptor(None, None, wd.English).language, wd.English)
        self.assertEqual(
            LexemeDescriptor().get_language(wd.English), wd.English)
        self.assertIsNone(LexemeDescriptor().get_language())


if __name__ == '__main__':
    TestModelDescriptorLexemeDescriptor.main()
