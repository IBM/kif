# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    AnnotationRecord,
    IRI,
    Normal,
    NoValueSnak,
    Property,
    ReferenceRecord,
    ReferenceRecordSet,
    SnakSet,
    SomeValueSnak,
)

from .tests import kif_TestCase, main


class TestModelAnnotationRecord(kif_TestCase):

    def test__init__(self):
        # bad arguments
        self.assertRaises(TypeError, AnnotationRecord, 0)
        self.assertRaises(TypeError, AnnotationRecord, 0, [], Normal)
        self.assertRaises(TypeError, AnnotationRecord, [], 0, Normal)
        self.assertRaises(TypeError, AnnotationRecord, [], [], 0)
        # good arguments
        self.assert_annotation_record(
            AnnotationRecord(), SnakSet(), ReferenceRecordSet(), Normal)
        quals = [NoValueSnak(Property('p')), Property('q')(IRI('x'))]
        refs = [
            ReferenceRecord(
                NoValueSnak(Property('p')),
                SomeValueSnak(Property('q')),
            ),
            ReferenceRecord(
                Property('p')(IRI('x')))]
        self.assert_annotation_record(
            AnnotationRecord(quals, refs, Normal),
            SnakSet(*quals), ReferenceRecordSet(*refs), Normal)


if __name__ == '__main__':
    main()
