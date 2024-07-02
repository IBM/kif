# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    AnnotationRecord,
    AnnotationRecordSet,
    IRI,
    Item,
    ItemTemplate,
    Normal,
    NoValueSnak,
    Preferred,
    Property,
    Quantity,
    ReferenceRecord,
    ReferenceRecordSet,
    SnakSet,
    SomeValueSnak,
    Text,
    ValueSet,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_ObjectSetTestCase


class Test(kif_ObjectSetTestCase):

    def test_children_class(self) -> None:
        assert_type(
            AnnotationRecordSet.children_class,
            type[AnnotationRecord])
        self.assertIs(AnnotationRecordSet.children_class, AnnotationRecord)

    def test_check(self) -> None:
        assert_type(
            AnnotationRecordSet.check([AnnotationRecord()]),
            AnnotationRecordSet)
        super()._test_check(
            AnnotationRecordSet,
            success=[
                ([], AnnotationRecordSet()),
                ([AnnotationRecord(), AnnotationRecord()],
                 AnnotationRecordSet(AnnotationRecord())),
                ([
                    AnnotationRecord(
                        [ValueSnak('x', 'y')],
                        [ReferenceRecord(SomeValueSnak('x'))],
                        Normal),
                    AnnotationRecord(
                        [ValueSnak('x', 'y')],
                        [ReferenceRecord()],
                        Normal)
                ],
                    AnnotationRecordSet(
                    AnnotationRecord(
                        SnakSet(ValueSnak('x', 'y')),
                        ReferenceRecordSet(
                            ReferenceRecord(SomeValueSnak('x'))),
                        Normal),
                    AnnotationRecord(
                        SnakSet(ValueSnak('x', 'y')),
                        ReferenceRecordSet(ReferenceRecord()),
                        Normal))),
            ],
            failure=[
                0,
                [0],
                [Quantity(0)],
                IRI('x'),
                Item(Variable('x')),
                Property('x'),
                ReferenceRecord(),
                ReferenceRecord(NoValueSnak('x')),
                ReferenceRecordSet(),
                SnakSet(),
                SnakSet(),
                ValueSet(0, 1, 2),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(
            AnnotationRecordSet(AnnotationRecord([NoValueSnak('x')])),
            AnnotationRecordSet)
        self._test__init__(
            AnnotationRecordSet,
            self.assert_annotation_record_set,
            success=[
                ([AnnotationRecord(rank=Preferred),
                  AnnotationRecord(),
                  AnnotationRecord([SomeValueSnak('x')]),
                  AnnotationRecord()],
                 AnnotationRecordSet(
                     AnnotationRecord(),
                     AnnotationRecord(rank=Preferred),
                     AnnotationRecord(SnakSet(SomeValueSnak('x'))))),
            ],
            failure=[
                [Item('x'), NoValueSnak('x')],
                [ItemTemplate(Variable('x'))],
                [ReferenceRecordSet()],
                [SnakSet()],
                [SomeValueSnak('x')],
                [Variable('x')],
                [Variable('x', Text)],
            ])

    def test_union(self) -> None:
        assert_type(AnnotationRecordSet().union(), AnnotationRecordSet)
        self.assert_annotation_record_set(
            AnnotationRecordSet().union(
                AnnotationRecordSet(), AnnotationRecordSet()))
        self.assert_annotation_record_set(
            AnnotationRecordSet(
                AnnotationRecord(SnakSet(SomeValueSnak('x')))).union(
                    AnnotationRecordSet(
                        AnnotationRecord([SomeValueSnak('x')]),
                        AnnotationRecord([NoValueSnak('y')])),
                AnnotationRecordSet(
                    AnnotationRecord([ValueSnak('z', 'w')]))),
            AnnotationRecord([NoValueSnak('y')]),
            AnnotationRecord([SomeValueSnak('x')]),
            AnnotationRecord([ValueSnak('z', 'w')]))


if __name__ == '__main__':
    Test.main()
