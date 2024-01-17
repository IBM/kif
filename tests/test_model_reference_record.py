# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    KIF_Object,
    NoValueSnak,
    Property,
    ReferenceRecord,
    SnakSet,
    SomeValueSnak,
)

from .tests import kif_TestCase, main


class TestModelReferenceRecord(kif_TestCase):

    def test__preprocess_arg_reference_record(self):
        refs = ReferenceRecord(
            NoValueSnak(Property('p')), Property('q')(IRI('x')))
        self.assertIs(refs, KIF_Object._preprocess_arg_reference_record(
            refs, 1))
        self.assertEqual(refs, KIF_Object._preprocess_arg_reference_record(
            SnakSet(*refs), 1))
        self.assertEqual(refs, KIF_Object._preprocess_arg_reference_record(
            list(refs), 1))

    def test__preprocess_optional_arg_reference_record(self):
        refs = ReferenceRecord(NoValueSnak(Property('p')))
        self.assertIs(
            refs, KIF_Object._preprocess_optional_arg_reference_record(
                refs, 1, None))
        self.assertIs(
            refs, KIF_Object._preprocess_optional_arg_reference_record(
                None, 1, refs))
        self.assertIsNone(
            KIF_Object._preprocess_optional_arg_reference_record(
                None, 1, None))
        self.assertEqual(
            refs, KIF_Object._preprocess_optional_arg_reference_record(
                list(refs), 1))

    def test__init__(self):
        self.assertFalse(bool(ReferenceRecord()))
        self.assertTrue(bool(ReferenceRecord(NoValueSnak(Property('p')))))
        self.assert_reference_record(ReferenceRecord())
        snaks = [
            NoValueSnak(Property('p')),
            Property('p')(IRI('x')),
        ]
        self.assert_reference_record(ReferenceRecord(*snaks), *snaks)

    def test__eq__(self):
        self.assertNotEqual(ReferenceRecord(), SnakSet())
        self.assertEqual(ReferenceRecord(), ReferenceRecord())
        self.assertEqual(
            ReferenceRecord(NoValueSnak(Property('p'))),
            ReferenceRecord(NoValueSnak(Property('p'))))
        self.assertEqual(
            ReferenceRecord(
                SomeValueSnak(Property('q')),
                NoValueSnak(Property('p'))),
            ReferenceRecord(
                NoValueSnak(Property('p')),
                SomeValueSnak(Property('q')),
                NoValueSnak(Property('p'))))
        self.assertNotEqual(
            ReferenceRecord(NoValueSnak(Property('p'))),
            ReferenceRecord(NoValueSnak(Property('q'))))


if __name__ == '__main__':
    main()
