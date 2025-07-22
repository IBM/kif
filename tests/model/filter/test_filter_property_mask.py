# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    AliasProperty,
    DescriptionProperty,
    Filter,
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    LexicalCategoryProperty,
    Property,
    PseudoProperty,
    SubtypeProperty,
    TypeProperty,
)
from kif_lib.typing import assert_type

from ...tests import KIF_ObjectTestCase


class Test(KIF_ObjectTestCase):

    def test_check(self) -> None:
        assert_type(Filter.PropertyMask.check(Property), Filter.PropertyMask)
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Filter.PropertyMask.check, {})
        self.assertRaisesRegex(
            ValueError, 'cannot coerce', Filter.PropertyMask.check,
            Filter.PropertyMask.ALL.value + 1)
        self.assertEqual(Filter.PropertyMask.check(0), Filter.PropertyMask(0))
        self.assertEqual(
            Filter.PropertyMask.check(Property),
            Filter.PropertyMask(Filter.PropertyMask.ALL))
        self.assertEqual(
            Filter.PropertyMask.check(PseudoProperty),
            Filter.PropertyMask(Filter.PSEUDO))
        self.assertEqual(
            Filter.PropertyMask.check(TypeProperty),
            Filter.PropertyMask(Filter.TYPE))
        self.assertEqual(
            Filter.PropertyMask.check(TypeProperty()),
            Filter.PropertyMask(Filter.TYPE))
        self.assertEqual(
            Filter.PropertyMask.check(SubtypeProperty),
            Filter.PropertyMask(Filter.SUBTYPE))
        self.assertEqual(
            Filter.PropertyMask.check(SubtypeProperty()),
            Filter.PropertyMask(Filter.SUBTYPE))
        self.assertEqual(
            Filter.PropertyMask.check(LabelProperty),
            Filter.PropertyMask(Filter.LABEL))
        self.assertEqual(
            Filter.PropertyMask.check(LabelProperty()),
            Filter.PropertyMask(Filter.LABEL))
        self.assertEqual(
            Filter.PropertyMask.check(AliasProperty),
            Filter.PropertyMask(Filter.ALIAS))
        self.assertEqual(
            Filter.PropertyMask.check(AliasProperty()),
            Filter.PropertyMask(Filter.ALIAS))
        self.assertEqual(
            Filter.PropertyMask.check(DescriptionProperty),
            Filter.PropertyMask(Filter.DESCRIPTION))
        self.assertEqual(
            Filter.PropertyMask.check(DescriptionProperty()),
            Filter.PropertyMask(Filter.DESCRIPTION))
        self.assertEqual(
            Filter.PropertyMask.check(LemmaProperty),
            Filter.PropertyMask(Filter.LEMMA))
        self.assertEqual(
            Filter.PropertyMask.check(LemmaProperty()),
            Filter.PropertyMask(Filter.LEMMA))
        self.assertEqual(
            Filter.PropertyMask.check(LexicalCategoryProperty),
            Filter.PropertyMask(Filter.LEXICAL_CATEGORY))
        self.assertEqual(
            Filter.PropertyMask.check(LexicalCategoryProperty()),
            Filter.PropertyMask(Filter.LEXICAL_CATEGORY))
        self.assertEqual(
            Filter.PropertyMask.check(LanguageProperty),
            Filter.PropertyMask(Filter.LANGUAGE))
        self.assertEqual(
            Filter.PropertyMask.check(LanguageProperty()),
            Filter.PropertyMask(Filter.LANGUAGE))
        self.assertEqual(
            Filter.PropertyMask.check_optional(
                None, Filter.PropertyMask.ALL),
            Filter.PropertyMask.ALL)
        self.assertIsNone(Filter.PropertyMask.check_optional(None))

    def test_match(self) -> None:
        assert_type(Filter.PropertyMask(0).match(TypeProperty()), bool)
        m = Filter.PropertyMask.ALL
        self.assertTrue(m.match(Property('x')))
        self.assertTrue(m.match(TypeProperty()))
        self.assertTrue(m.match(SubtypeProperty()))
        self.assertTrue(m.match(LabelProperty()))
        self.assertTrue(m.match(AliasProperty()))
        self.assertTrue(m.match(DescriptionProperty()))
        self.assertTrue(m.match(LemmaProperty()))
        self.assertTrue(m.match(LexicalCategoryProperty()))
        self.assertTrue(m.match(LanguageProperty()))
        m = Filter.REAL
        self.assertTrue(m.match(Property('x')))
        self.assertFalse(m.match(TypeProperty()))
        self.assertFalse(m.match(SubtypeProperty()))
        self.assertFalse(m.match(LabelProperty()))
        self.assertFalse(m.match(AliasProperty()))
        self.assertFalse(m.match(DescriptionProperty()))
        self.assertFalse(m.match(LemmaProperty()))
        self.assertFalse(m.match(LexicalCategoryProperty()))
        self.assertFalse(m.match(LanguageProperty()))
        m = Filter.PSEUDO
        self.assertFalse(m.match(Property('x')))
        self.assertTrue(m.match(TypeProperty()))
        self.assertTrue(m.match(SubtypeProperty()))
        self.assertTrue(m.match(LabelProperty()))
        self.assertTrue(m.match(AliasProperty()))
        self.assertTrue(m.match(DescriptionProperty()))
        self.assertTrue(m.match(LemmaProperty()))
        self.assertTrue(m.match(LexicalCategoryProperty()))
        self.assertTrue(m.match(LanguageProperty()))
        m = Filter.TYPE | Filter.LABEL | Filter.LEXICAL_CATEGORY
        self.assertFalse(m.match(Property('x')))
        self.assertTrue(m.match(TypeProperty()))
        self.assertFalse(m.match(SubtypeProperty()))
        self.assertTrue(m.match(LabelProperty()))
        self.assertFalse(m.match(AliasProperty()))
        self.assertFalse(m.match(DescriptionProperty()))
        self.assertFalse(m.match(LemmaProperty()))
        self.assertTrue(m.match(LexicalCategoryProperty()))
        self.assertFalse(m.match(LanguageProperty()))


if __name__ == '__main__':
    Test.main()
