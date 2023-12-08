# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif import (
    IRI,
    KIF_Object,
    NoValueSnak,
    Property,
    ReferenceRecord,
    ReferenceRecordSet,
    SnakSet,
    SomeValueSnak,
)

from .tests import kif_TestCase, main


class TestModelReferenceRecordSet(kif_TestCase):

    def test__preprocess_arg_reference_record_set(self):
        refs = ReferenceRecordSet(
            [NoValueSnak(Property('p')), Property('q')(IRI('x'))],
            ReferenceRecord(SomeValueSnak(Property('p'))))
        self.assertIs(
            refs, KIF_Object._preprocess_arg_reference_record_set(refs, 1))
        self.assertEqual(
            refs, KIF_Object._preprocess_arg_reference_record_set(
                list(refs), 1))

    def test__preprocess_optional_arg_reference_record_set(self):
        refs = ReferenceRecordSet(
            [NoValueSnak(Property('p'))],
            SnakSet(SomeValueSnak(Property('p'))))
        self.assertIs(
            refs,
            KIF_Object._preprocess_optional_arg_reference_record_set(
                refs, 1, None))
        self.assertIs(
            refs,
            KIF_Object._preprocess_optional_arg_reference_record_set(
                None, 1, refs))
        self.assertIsNone(
            KIF_Object._preprocess_optional_arg_reference_record_set(
                None, 1, None))
        self.assertEqual(
            refs,
            KIF_Object._preprocess_optional_arg_reference_record_set(
                list(refs), 1))

    def test__init__(self):
        self.assertRaises(TypeError, ReferenceRecordSet, 0)
        self.assertRaises(TypeError, ReferenceRecordSet, Property('p'))
        self.assertRaises(
            TypeError, ReferenceRecordSet, SomeValueSnak(Property('p')))
        self.assertFalse(bool(ReferenceRecordSet()))
        self.assertTrue(bool(ReferenceRecordSet(
            SnakSet(NoValueSnak(Property('p'))))))
        self.assert_reference_record_set(ReferenceRecordSet())
        refs = [
            ReferenceRecord(NoValueSnak(Property('p')),
                            Property('p')(IRI('x'))),
            ReferenceRecord(NoValueSnak(Property('q')))
        ]
        self.assert_reference_record_set(
            ReferenceRecordSet(*refs), *refs)

    def test__contains__(self):
        self.assertNotIn(0, ReferenceRecordSet())
        self.assertIn(
            ReferenceRecord(NoValueSnak(Property('p'))),
            ReferenceRecordSet(ReferenceRecord(NoValueSnak(Property('p')))))
        self.assertNotIn(
            ReferenceRecord(NoValueSnak(Property('p'))),
            ReferenceRecordSet(ReferenceRecord(NoValueSnak(Property('q')))))

    def test_union(self):
        s1 = ReferenceRecordSet(
            ReferenceRecord(Property('p')(IRI('x'))),
            ReferenceRecord(Property('q')(IRI('y'))))
        s2 = ReferenceRecordSet(ReferenceRecord(NoValueSnak(Property('p'))))
        s3 = ReferenceRecordSet()
        s4 = ReferenceRecordSet(
            ReferenceRecord(Property('q')(IRI('y'))),
            ReferenceRecord(Property('q')(IRI('z'))))
        self.assertEqual(
            s1.union(s2, s3, s4),
            ReferenceRecordSet(
                *map(ReferenceRecord, [
                    NoValueSnak(Property('p')),
                    Property('p')(IRI('x')),
                    Property('q')(IRI('y')),
                    Property('q')(IRI('z'))])))


if __name__ == '__main__':
    main()
