# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    EntityFingerprint,
    Filter,
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


class TestModelPatternFilter(kif_TestCase):

    def test_from_snak(self):
        # snak is none
        pat = Filter.from_snak(Item('x'), None)
        self.assert_filter_pattern(
            pat, EntityFingerprint(Item('x')), None, None, Snak.ALL)
        # value snak
        snak = Property('p')(Item('x'))
        pat = Filter.from_snak(Item('x'), snak)
        self.assert_filter_pattern(
            pat,
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p', Item)),
            Fingerprint(Item('x')),
            Snak.VALUE_SNAK)
        # some value snak
        snak = SomeValueSnak(Property('p'))
        pat = Filter.from_snak(Item('x'), snak)
        self.assert_filter_pattern(
            pat,
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            None,
            Snak.SOME_VALUE_SNAK)
        # no value snak
        snak = NoValueSnak(Property('p'))
        pat = Filter.from_snak(Item('x'), snak)
        self.assert_filter_pattern(
            pat,
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            None,
            Snak.NO_VALUE_SNAK)

    def test_from_statement(self):
        # value snak
        stmt = Property('p')(Item('x'), IRI('y'))
        pat = Filter.from_statement(stmt)
        self.assert_filter_pattern(
            pat,
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p', IRI)),
            Fingerprint(IRI('y')),
            Snak.VALUE_SNAK)
        # some value snak
        stmt = Statement(Item('x'), SomeValueSnak(Property('p')))
        pat = Filter.from_statement(stmt)
        self.assert_filter_pattern(
            pat,
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            None,
            Snak.SOME_VALUE_SNAK)
        # no value snak
        stmt = Statement(Item('x'), NoValueSnak(Property('p')))
        pat = Filter.from_statement(stmt)
        self.assert_filter_pattern(
            pat,
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            None,
            Snak.NO_VALUE_SNAK)

    def test__init__(self):
        self.assertRaises(TypeError, Filter, 0)
        self.assert_filter_pattern(Filter())

    def test_is_empty(self):
        self.assertFalse(Filter().is_empty())
        self.assertTrue(Filter().is_nonempty())
        self.assertTrue(Filter().is_full())
        self.assertTrue(Filter(None, None, None, 0).is_empty())
        self.assertFalse(Filter(None, None, None, 0).is_nonempty())
        pat = Filter(None, None, IRI('x'), Snak.SOME_VALUE_SNAK)
        self.assertTrue(pat.is_empty())
        self.assertFalse(pat.is_nonempty())
        pat = Filter(None, None, IRI('x'), Snak.NO_VALUE_SNAK)
        self.assertTrue(pat.is_empty())
        self.assertFalse(pat.is_nonempty())

    def test_is_full(self):
        self.assertTrue(Filter().is_full())
        self.assertFalse(Filter().is_nonfull())

    def test_combine(self):
        # bad argument
        pat = Filter(Item('x'))
        self.assertRaises(TypeError, pat.combine, 0)
        # bad argument: incompatible subjects
        pat1 = Filter(Item('x'))
        pat2 = Filter(SnakSet())
        self.assertRaisesRegex(
            ValueError, 'subjects cannot be combined', pat1.combine, pat2)
        # bad argument: incompatible predicates
        pat1 = Filter(None, SnakSet(NoValueSnak(Property('x'))))
        pat2 = Filter(None, Property('p'))
        self.assertRaisesRegex(
            ValueError, 'properties cannot be combined', pat1.combine, pat2)
        # bad argument: incompatible values
        pat1 = Filter(None, None, SnakSet(NoValueSnak(Property('x'))))
        pat2 = Filter(None, None, Property('p'))
        self.assertRaisesRegex(
            ValueError, 'values cannot be combined', pat1.combine, pat2)
        # good arguments
        self.assertEqual(Filter().combine(), Filter())
        self.assertEqual(
            Filter().combine(Filter()), Filter())
        # subject
        pat1 = Filter(Item('x'))
        pat2 = Filter(None, Property('p'))
        self.assertEqual(
            pat1.combine(pat2),
            Filter(Item('x'), Property('p')))
        pat1 = Filter(SnakSet(SomeValueSnak(Property('p'))))
        pat2 = Filter(SnakSet(NoValueSnak(Property('q'))))
        self.assertEqual(
            pat1.combine(pat2),
            Filter([
                SomeValueSnak(Property('p')),
                NoValueSnak(Property('q'))]))
        # property
        pat1 = Filter(None, Property('p'))
        pat2 = Filter(Item('x'))
        self.assertEqual(
            pat1.combine(pat2),
            Filter(Item('x'), Property('p')))
        pat1 = Filter(None, SnakSet(SomeValueSnak(Property('p'))))
        pat2 = Filter(None, SnakSet(NoValueSnak(Property('q'))))
        self.assertEqual(
            pat1.combine(pat2),
            Filter(None, [
                SomeValueSnak(Property('p')),
                NoValueSnak(Property('q'))]))
        # value
        pat1 = Filter(None, Property('p'), IRI('x'))
        pat2 = Filter(Item('x'), None, None)
        self.assertEqual(
            pat1.combine(pat2),
            Filter(Item('x'), Property('p'), IRI('x')))
        pat1 = Filter(
            None, None, SnakSet(SomeValueSnak(Property('p'))))
        pat2 = Filter(
            None, None, SnakSet(NoValueSnak(Property('q'))))
        self.assertEqual(
            pat1.combine(pat2),
            Filter(None, None, [
                SomeValueSnak(Property('p')),
                NoValueSnak(Property('q'))]))
        # snak mask
        self.assertEqual(
            Filter(None, None, None, Snak.ALL).combine(
                Filter(None, None, None, Snak.VALUE_SNAK)),
            Filter(None, None, None, Snak.VALUE_SNAK))


if __name__ == '__main__':
    TestModelPatternFilter.main()
