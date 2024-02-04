# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.vocabulary as wd
from kif_lib import LexemeDescriptor, Text

from .tests import kif_TestCase, main


class TestModelLexemeDescriptor(kif_TestCase):

    def test__init__(self):
        # bad arguments
        self.assertRaises(TypeError, LexemeDescriptor, 0)
        self.assertRaises(TypeError, LexemeDescriptor, 'x', wd.English)
        self.assertRaises(TypeError, LexemeDescriptor, 'x', 0, wd.verb)
        self.assertRaises(TypeError, LexemeDescriptor, 'x', wd.verb, wd.mass)
        # good arguments
        self.assert_lexeme_descriptor(
            LexemeDescriptor('x', wd.verb, wd.English),
            Text('x'), wd.verb, wd.English)

    def test_get_lemma(self):
        desc = LexemeDescriptor('x', wd.verb, wd.English)
        self.assertEqual(desc.get_lemma(), Text('x'))
        self.assertEqual(desc.lemma, Text('x'))

    def test_get_category(self):
        desc = LexemeDescriptor('x', wd.verb, wd.English)
        self.assertEqual(desc.get_category(), wd.verb)
        self.assertEqual(desc.category, wd.verb)

    def test_get_language(self):
        desc = LexemeDescriptor('x', wd.verb, wd.English)
        self.assertEqual(desc.get_language(), wd.English)
        self.assertEqual(desc.language, wd.English)


if __name__ == '__main__':
    main()
