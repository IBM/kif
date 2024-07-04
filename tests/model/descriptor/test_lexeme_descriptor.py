# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    ItemDescriptor,
    LexemeDescriptor,
    PropertyDescriptor,
    String,
    Text,
)
from kif_lib.typing import assert_type
from kif_lib.vocabulary import wd

from ...tests import kif_DescriptorTestCase


class Test(kif_DescriptorTestCase):

    def test_check(self) -> None:
        assert_type(
            LexemeDescriptor.check(LexemeDescriptor()), LexemeDescriptor)
        self._test_check(
            LexemeDescriptor,
            success=[
                (LexemeDescriptor(), LexemeDescriptor()),
                (LexemeDescriptor('x'), LexemeDescriptor(Text('x'))),
                (LexemeDescriptor(None, 'y'),
                 LexemeDescriptor(None, Item('y'))),
                (LexemeDescriptor(None, None, IRI('z')),
                 LexemeDescriptor(None, None, Item('z'))),
                (LexemeDescriptor(String('x'), IRI('y'), 'z'),
                 LexemeDescriptor('x', Item('y'), Item('z'))),
            ],
            failure=[ItemDescriptor(), PropertyDescriptor()])

    def test__init__(self) -> None:
        assert_type(LexemeDescriptor(), LexemeDescriptor)
        self._test__init__(
            LexemeDescriptor,
            self.assert_lexeme_descriptor,
            success=[
                ([], LexemeDescriptor()),
                ([None, None, 'x'],
                 LexemeDescriptor(language=Item('x'))),
                ([ExternalId('x'), IRI('y')],
                 LexemeDescriptor(Text('x'), Item('y'))),
                ([Text('x', 'es'), None, String('y')],
                 LexemeDescriptor(Text('x', 'es'), None, Item('y'))),
            ])

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
    Test.main()
