# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.vocabulary as wd
from kif_lib import (
    AnnotationRecord,
    AnnotationRecordSet,
    KIF_Object,
    Normal,
    Preferred,
    Property,
    ReferenceRecord,
    SomeValueSnak,
)

from .tests import kif_TestCase, main


class TestModelAnnotationRecordSet(kif_TestCase):

    def test__preprocess_arg_annotation_record_set(self):
        annots = AnnotationRecordSet(
            AnnotationRecord(
                [wd.country(wd.Brazil)], [], Normal),
            AnnotationRecord(
                [], [ReferenceRecord(wd.country(wd.Brazil))], Normal))
        self.assertIs(
            annots,
            KIF_Object._preprocess_arg_annotation_record_set(annots, 1))
        self.assertEqual(
            annots, KIF_Object._preprocess_arg_annotation_record_set(
                list(annots), 1))

    def test__preprocess_optional_annotation_record_set(self):
        annots = AnnotationRecordSet(
            AnnotationRecord(
                [wd.country(wd.Brazil)], [], Normal),
            AnnotationRecord(
                [], [ReferenceRecord(wd.country(wd.Brazil))], Normal))
        self.assertIs(
            annots,
            KIF_Object._preprocess_optional_arg_annotation_record_set(
                annots, 1, None))
        self.assertIs(
            annots,
            KIF_Object._preprocess_optional_arg_annotation_record_set(
                None, 1, annots))
        self.assertIsNone(
            KIF_Object._preprocess_optional_arg_annotation_record_set(
                None, 1, None))
        self.assertEqual(
            annots,
            KIF_Object._preprocess_optional_arg_annotation_record_set(
                list(annots), 1))

    def test__init__(self):
        self.assertRaises(TypeError, AnnotationRecordSet, 0)
        self.assertRaises(TypeError, AnnotationRecordSet, Property('p'))
        self.assertRaises(
            TypeError, AnnotationRecordSet, SomeValueSnak(Property('p')))
        self.assertFalse(bool(AnnotationRecordSet()))
        self.assertTrue(bool(AnnotationRecordSet(
            AnnotationRecord([], [], Normal))))
        self.assert_annotation_record_set(AnnotationRecordSet())
        annots = [
            AnnotationRecord(
                [], [ReferenceRecord(wd.country(wd.Brazil))], Normal),
            AnnotationRecord(
                [wd.country(wd.Brazil)], [], Normal),
        ]
        self.assert_annotation_record_set(
            AnnotationRecordSet(*annots), *annots)

    def test__contains__(self):
        self.assertNotIn(0, AnnotationRecordSet())
        self.assertIn(
            AnnotationRecord([], [], Normal),
            AnnotationRecordSet(AnnotationRecord([], [], Normal)))
        self.assertNotIn(
            AnnotationRecord([], [], Preferred),
            AnnotationRecordSet(AnnotationRecord([], [], Normal)))

    def test_union(self):
        s1 = AnnotationRecordSet(
            AnnotationRecord(
                [wd.country(wd.Brazil)], [], Normal),
            AnnotationRecord(
                [], [ReferenceRecord(wd.country(wd.Brazil))], Normal))
        s2 = AnnotationRecordSet(
            AnnotationRecord(
                [wd.continent(wd.South_America)], [], Normal))
        s3 = AnnotationRecordSet()
        s4 = AnnotationRecordSet(
            AnnotationRecord(
                [wd.country(wd.Brazil)], [], Normal))
        self.assertEqual(
            s1.union(s2, s3, s4),
            AnnotationRecordSet(
                *[AnnotationRecord(
                    [wd.country(wd.Brazil)], [], Normal),
                  AnnotationRecord(
                      [], [ReferenceRecord(wd.country(wd.Brazil))], Normal),
                  AnnotationRecord(
                      [wd.continent(wd.South_America)], [], Normal)]))


if __name__ == '__main__':
    main()
