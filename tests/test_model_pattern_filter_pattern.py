# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    EntityFingerprint,
    FilterPattern,
    Fingerprint,
    IRI,
    Item,
    NoValueSnak,
    Property,
    PropertyFingerprint,
    Snak,
    SnakSet,
    SomeValueSnak,
    Statement,
)

from .tests import kif_TestCase


class TestModelPatternFilterPattern(kif_TestCase):

    def test_from_snak(self):
        # snak is none
        pat = FilterPattern.from_snak(Item('x'), None)
        self.assert_filter_pattern(
            pat, EntityFingerprint(Item('x')), None, None, Snak.ALL)
        # value snak
        snak = Property('p')(Item('x'))
        pat = FilterPattern.from_snak(Item('x'), snak)
        self.assert_filter_pattern(
            pat,
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            Fingerprint(Item('x')),
            Snak.VALUE_SNAK)
        # some value snak
        snak = SomeValueSnak(Property('p'))
        pat = FilterPattern.from_snak(Item('x'), snak)
        self.assert_filter_pattern(
            pat,
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            None,
            Snak.SOME_VALUE_SNAK)
        # no value snak
        snak = NoValueSnak(Property('p'))
        pat = FilterPattern.from_snak(Item('x'), snak)
        self.assert_filter_pattern(
            pat,
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            None,
            Snak.NO_VALUE_SNAK)

    def test_from_statement(self):
        # value snak
        stmt = Property('p')(Item('x'), IRI('y'))
        pat = FilterPattern.from_statement(stmt)
        self.assert_filter_pattern(
            pat,
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            Fingerprint(IRI('y')),
            Snak.VALUE_SNAK)
        # some value snak
        stmt = Statement(Item('x'), SomeValueSnak(Property('p')))
        pat = FilterPattern.from_statement(stmt)
        self.assert_filter_pattern(
            pat,
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            None,
            Snak.SOME_VALUE_SNAK)
        # no value snak
        stmt = Statement(Item('x'), NoValueSnak(Property('p')))
        pat = FilterPattern.from_statement(stmt)
        self.assert_filter_pattern(
            pat,
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            None,
            Snak.NO_VALUE_SNAK)

    def test__init__(self):
        self.assertRaises(TypeError, FilterPattern, 0)
        self.assert_filter_pattern(FilterPattern())

    def test_is_empty(self):
        self.assertFalse(FilterPattern().is_empty())
        self.assertTrue(FilterPattern().is_nonempty())
        self.assertTrue(FilterPattern().is_full())
        self.assertTrue(FilterPattern(None, None, None, 0).is_empty())
        self.assertFalse(FilterPattern(None, None, None, 0).is_nonempty())
        pat = FilterPattern(None, None, IRI('x'), Snak.SOME_VALUE_SNAK)
        self.assertTrue(pat.is_empty())
        self.assertFalse(pat.is_nonempty())
        pat = FilterPattern(None, None, IRI('x'), Snak.NO_VALUE_SNAK)
        self.assertTrue(pat.is_empty())
        self.assertFalse(pat.is_nonempty())

    def test_is_full(self):
        self.assertTrue(FilterPattern().is_full())
        self.assertFalse(FilterPattern().is_nonfull())

    def test_combine(self):
        # bad argument
        pat = FilterPattern(Item('x'))
        self.assertRaises(TypeError, pat.combine, 0)
        # bad argument: incompatible subjects
        pat1 = FilterPattern(Item('x'))
        pat2 = FilterPattern(SnakSet())
        self.assertRaisesRegex(
            ValueError, 'subjects cannot be combined', pat1.combine, pat2)
        # bad argument: incompatible predicates
        pat1 = FilterPattern(None, SnakSet(NoValueSnak(Property('x'))))
        pat2 = FilterPattern(None, Property('p'))
        self.assertRaisesRegex(
            ValueError, 'properties cannot be combined', pat1.combine, pat2)
        # bad argument: incompatible values
        pat1 = FilterPattern(None, None, SnakSet(NoValueSnak(Property('x'))))
        pat2 = FilterPattern(None, None, Property('p'))
        self.assertRaisesRegex(
            ValueError, 'values cannot be combined', pat1.combine, pat2)
        # good arguments
        self.assertEqual(FilterPattern().combine(), FilterPattern())
        self.assertEqual(
            FilterPattern().combine(FilterPattern()), FilterPattern())
        # subject
        pat1 = FilterPattern(Item('x'))
        pat2 = FilterPattern(None, Property('p'))
        self.assertEqual(
            pat1.combine(pat2),
            FilterPattern(Item('x'), Property('p')))
        pat1 = FilterPattern(SnakSet(SomeValueSnak(Property('p'))))
        pat2 = FilterPattern(SnakSet(NoValueSnak(Property('q'))))
        self.assertEqual(
            pat1.combine(pat2),
            FilterPattern([
                SomeValueSnak(Property('p')),
                NoValueSnak(Property('q'))]))
        # property
        pat1 = FilterPattern(None, Property('p'))
        pat2 = FilterPattern(Item('x'))
        self.assertEqual(
            pat1.combine(pat2),
            FilterPattern(Item('x'), Property('p')))
        pat1 = FilterPattern(None, SnakSet(SomeValueSnak(Property('p'))))
        pat2 = FilterPattern(None, SnakSet(NoValueSnak(Property('q'))))
        self.assertEqual(
            pat1.combine(pat2),
            FilterPattern(None, [
                SomeValueSnak(Property('p')),
                NoValueSnak(Property('q'))]))
        # value
        pat1 = FilterPattern(None, Property('p'), IRI('x'))
        pat2 = FilterPattern(Item('x'), None, None)
        self.assertEqual(
            pat1.combine(pat2),
            FilterPattern(Item('x'), Property('p'), IRI('x')))
        pat1 = FilterPattern(
            None, None, SnakSet(SomeValueSnak(Property('p'))))
        pat2 = FilterPattern(
            None, None, SnakSet(NoValueSnak(Property('q'))))
        self.assertEqual(
            pat1.combine(pat2),
            FilterPattern(None, None, [
                SomeValueSnak(Property('p')),
                NoValueSnak(Property('q'))]))
        # snak mask
        self.assertEqual(
            FilterPattern(None, None, None, Snak.ALL).combine(
                FilterPattern(None, None, None, Snak.VALUE_SNAK)),
            FilterPattern(None, None, None, Snak.VALUE_SNAK))


if __name__ == '__main__':
    TestModelPatternFilterPattern.main()
